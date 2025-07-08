import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
from datetime import datetime
from pytz import timezone
import io
import contextlib
import os

def gestion():
    
    st.title('Análisis de datos de Gestores Operativos')
    
    archivo_datos_inc = st.file_uploader("subir Incidentes CSV", type=["csv", "xlsx"])

    if archivo_datos_inc is not None:
        try:
            detalle_archivo = {
                "Nombre del archivo": archivo_datos_inc.name,
                "Tipo de archivo": archivo_datos_inc.type,
                "Tamaño del archivo": archivo_datos_inc.size
            }
            #st.write(detalle_archivo)

            if detalle_archivo["Tipo de archivo"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df_incidentes = pd.read_excel(archivo_datos_inc, engine="openpyxl")
            elif detalle_archivo["Tipo de archivo"] == "text/csv":
                df_incidentes = pd.read_csv(archivo_datos_inc, sep=';', skiprows=3)
            else:
                st.error("Formato de archivo no soportado.")
                return

            if df_incidentes.empty:
                st.warning("El archivo cargado está vacío.")
                return
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")

        
    archivo_datos = st.file_uploader("subir WFM excel", type=["csv", "xlsx"])

    if archivo_datos is not None:
        try:
            detalle_archivo = {
                "Nombre del archivo": archivo_datos.name,
                "Tipo de archivo": archivo_datos.type,
                "Tamaño del archivo": archivo_datos.size
            }
            #st.write(detalle_archivo)

            if detalle_archivo["Tipo de archivo"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df_wfm = pd.read_excel(archivo_datos, engine="openpyxl")
            elif detalle_archivo["Tipo de archivo"] == "text/csv":
                df_wfm = pd.read_csv(archivo_datos, sep=';', skiprows=3)
            else:
                st.error("Formato de archivo no soportado.")
                return

            if df_wfm.empty:
                st.warning("El archivo cargado está vacío.")
                return
        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")


    if archivo_datos_inc is not None:

        # Eliminar los excluibles
        df_incidentes = df_incidentes[~df_incidentes['Causa'].str.startswith('Exc_')]

        # Cambiar tipo de dato a fecha para la columna 'Fecha de interrupción'
        df_incidentes['Fecha de interrupción'] = pd.to_datetime(df_incidentes['Fecha de interrupción'], dayfirst=True, errors='coerce')

        # Diccionario de meses
        meses = {
            1: "enero", 
            2: "febrero", 
            3: "marzo", 
            4: "abril",
            5: "mayo", 
            6: "junio", 
            7: "julio", 
            8: "agosto",
            9: "septiembre", 
            10: "octubre", 
            11: "noviembre", 
            12: "diciembre"
        }

        # Crear columna 'Fecha de interrupción (formato texto)' para mostrar la fecha en el formato deseado
        df_incidentes['Fecha de interrupción (texto)'] = df_incidentes['Fecha de interrupción'].dt.day.astype(str) + ' de ' + df_incidentes['Fecha de interrupción'].dt.month.map(meses)

        # Realizar reemplazos de texto según informe de salida
        df_incidentes['Identificación'] = df_incidentes['Identificación'].str.replace('INC ', '')
        df_incidentes['Sector'] = df_incidentes['Sector'].str.replace('CELSIA - ', '').str.replace('CETSA - TODO', 'Valle Cetsa')
        df_incidentes['Grupo AOR'] = df_incidentes['Grupo AOR'].str.replace('CO-TOL-DI-CELSIA-TNORTE-CENTRO', 'Tolima Centro')\
            .str.replace('CO-TOL-DI-CELSIA-TNORTE-NORTE', 'Tolima Norte')\
            .str.replace('CO-TOL-DI-CELSIA-TSUR-ORIENTE', 'Tolima Oriente')\
            .str.replace('CO-TOL-DI-CELSIA-TSUR-SUR', 'Tolima Sur')\
            .str.replace('CO-VAC-DI-CETSA-VNORTE-CETSA', 'Valle Cetsa')\
            .str.replace('CO-VAC-DI-EPSA-VNORTE-CENTRO', 'Valle Centro')\
            .str.replace('CO-VAC-DI-EPSA-VNORTE-NORTE', 'Valle Norte')\
            .str.replace('CO-VAC-DI-EPSA-VSUR-PACIFICO', 'Valle Pacifico')\
            .str.replace('CO-VAC-DI-EPSA-VSUR-SUR', 'Valle Sur')



        # Llenar valores nulos en 'Sector' con los de 'Grupo AOR'
        df_incidentes['Sector'] = df_incidentes['Sector'].fillna(df_incidentes['Grupo AOR'])
        df_incidentes['Sector'] = df_incidentes['Sector'].str.title()


        # Agrupar por Sector e Identificación y obtener la fecha mínima de creación
        df_fecha_min = df_incidentes.groupby(['Sector', 'Identificación'])['Fecha de interrupción'].min().reset_index()

        # Ordenar el resultado por la Fecha de interrupción
        df_fecha_min = df_fecha_min.sort_values(by='Fecha de interrupción')

        # Crear un DataFrame para las otras columnas que necesitas
        df_id = df_incidentes[['Sector', 'Identificación', 'Fecha de interrupción', 'Causa']]
        df_id.set_index('Sector', inplace=True)

        # Obtener fecha y hora actual
        fecha_y_hora_actuales = datetime.now()
        zona_horaria = timezone('America/Bogota')
        hora_actual = fecha_y_hora_actuales.astimezone(zona_horaria).strftime('%H:%M')
        fecha_actual = fecha_y_hora_actuales.strftime('%d/%m/%Y')


        lista_incidentes = df_incidentes['Sector'].value_counts()

        # Función para formatear la fecha como "12 de noviembre"
        def formatear_fecha(fecha):
            return f'{fecha.day} de {meses[fecha.month]}'

        # Inicializar lista para los resultados
        lista = []

        # Iterar sobre los sectores y las incidencias (usando lista_incidentes)
        for key, value in lista_incidentes.to_dict().items():
            # Normalizar la clave 'key' para evitar problemas de formato
            key_normalized = key.strip().title()

            if value > 1:
                # Acceder a las fechas más antiguas y causas correspondientes al sector e identificación
                if key_normalized in df_fecha_min['Sector'].values:
                    # Obtener el incidente más antiguo para el sector
                    fecha_min = df_fecha_min[df_fecha_min['Sector'] == key_normalized].min()['Fecha de interrupción']
                else:
                    fecha_min = 'No disponible'

                # Formatear la fecha de la forma "12 de noviembre"
                if isinstance(fecha_min, pd.Timestamp):
                    fecha_min = formatear_fecha(fecha_min)

                if key_normalized in df_id.index:
                    # Obtener la Identificación y Causa del incidente más antiguo
                    identificacion = df_id[df_id.index == key_normalized].iloc[0]['Identificación']
                    causa = df_id[df_id.index == key_normalized].iloc[0]['Causa']
                else:
                    identificacion = 'No disponible'
                    causa = 'No disponible'

                # Añadir solo el incidente más antiguo al listado
                lista.append((key, value, fecha_min, identificacion, causa))
            else:
                # Si solo hay un incidente, añadirlo directamente
                if key_normalized in df_fecha_min['Sector'].values:
                    fecha_min = df_fecha_min[df_fecha_min['Sector'] == key_normalized].min()['Fecha de interrupción']
                else:
                    fecha_min = 'No disponible'

                if isinstance(fecha_min, pd.Timestamp):
                    fecha_min = formatear_fecha(fecha_min)

                if key_normalized in df_id.index:
                    identificacion = df_id[df_id.index == key_normalized].iloc[0]['Identificación']
                    causa = df_id[df_id.index == key_normalized].iloc[0]['Causa']
                else:
                    identificacion = 'No disponible'
                    causa = 'No disponible'

                lista.append((key, value, fecha_min, identificacion, causa))

        # Filtrar por "Valle" y "Tolima"
        lista_valle = sorted([i for i in lista if 'Valle' in i[0]], key=lambda x: (x[0]))  # Ordenar por nombre de zona alfabéticamente
        total_valle = sum([i[1] for i in lista_valle])

        lista_tolima = sorted([i for i in lista if 'Tolima' in i[0]], key=lambda x: (x[0]))  # Ordenar por nombre de zona alfabéticamente
        total_tolima = sum([i[1] for i in lista_tolima])

        # Crear el output usando StringIO para redirigir la salida
        output_inc = io.StringIO()
        with contextlib.redirect_stdout(output_inc):
            print(f'*Con corte en el ADMS a las {hora_actual}, tenemos {sum(lista_incidentes.values)} incidentes pendientes*\n')

            # Imprimir los incidentes para Valle, solo el más antiguo por sector
            print(f' *Para Valle tenemos {total_valle} pendientes mtto, distribuidos por sector así:*\n')
            for i in lista_valle:
                print(f' - {i[0]}: {i[1]} (más antiguo del {i[2]} INC {i[3]} - {i[4]})')
            print("\n")
            # Imprimir los incidentes para Tolima, solo el más antiguo por sector
            print(f' *Para Tolima tenemos {total_tolima} pendientes mtto, distribuidos por sector así:*\n')
            for i in lista_tolima:
                print(f' - {i[0]}: {i[1]} (más antiguo del {i[2]} INC {i[3]} - {i[4]})')
            print(f'\n')
           

        # Obtener el valor del output generado
        inc = output_inc.getvalue()

        # ------------------------------------------------------------------------------
        # Renombrar CETSA y Pacífico
        inc = output_inc.getvalue()
        inc = inc.replace("Valle Cetsa", "CETSA")
        inc = inc.replace("Valle Pacifico", "Pacífico")
        # ------------------------------------------------------------------------------
        output_inc.close()

        #print(identificacion)

        # Filtrar los incidentes por causa de 'Transformador distribución averiado'
        df_causa = df_incidentes[df_incidentes['Causa'] == 'Transformador distribución averiado']

        # Contar los sectores con la causa
        lista_causa = df_causa['Sector'].value_counts()

        # Obtener la fecha mínima por sector (la fecha más antigua de interrupción)
        df_fecha_min_causa = df_causa.groupby(['Sector'])['Fecha de interrupción'].min()

        # Extraer los datos de identificación y causa
        df_id2 = df_causa[['Sector', 'Identificación', 'Fecha de interrupción', 'Causa']]
        df_id2.set_index('Sector', inplace=True)

        # Calcular el total de incidentes por causa
        total_causa = sum(lista_causa.to_dict().values())

        # Crear la lista para almacenar los incidentes
        lista_2 = []

        # Procesar cada sector y agregar la información relevante
        for key, value in lista_causa.to_dict().items():
            # Obtener la fecha mínima para cada sector
            fecha_min = df_fecha_min_causa.get(key, None)

            # Si no hay fecha mínima, continuar con el siguiente sector
            if fecha_min is None:
                lista_2.append((key, value, 'No disponible', 'No disponible'))
                continue

            # Formatear la fecha usando la función formatear_fecha
            if isinstance(fecha_min, pd.Timestamp):
                fecha_min_formateada = formatear_fecha(fecha_min)
            else:
                fecha_min_formateada = 'No disponible'

            # Filtrar los incidentes de ese sector y obtener el más antiguo
            df_sector = df_causa[df_causa['Sector'] == key]
            df_sector_min_fecha = df_sector[df_sector['Fecha de interrupción'] == fecha_min]

            # Comprobar si hay incidentes disponibles
            if not df_sector_min_fecha.empty:
                # Obtener la identificación del incidente más antiguo en ese sector
                identificacion = df_sector_min_fecha.iloc[0]['Identificación']
                lista_2.append((key, value, fecha_min_formateada, identificacion))
            else:
                # Si no hay incidentes, agregar 'No disponible'
                lista_2.append((key, value, fecha_min_formateada, 'No disponible'))

        # Filtrar incidentes por zona: Valle y Tolima
        lista_valle_tr = sorted([i for i in lista_2 if 'Valle' in i[0]], key=lambda x: x[0])
        lista_tolima_tr = sorted([i for i in lista_2 if 'Tolima' in i[0]], key=lambda x: x[0])

        # Crear la salida con el formato adecuado
        output_inc_tr = io.StringIO()
        with contextlib.redirect_stdout(output_inc_tr):
            # Imprimir el total de incidentes por causa
        
               
            print(f' *Por causa de transformador de distribución averiado, tenemos un total de {total_causa}.*')
            # Imprimir los incidentes para Valle
            for i in lista_valle_tr:
                print(f'- {i[0]}: {i[1]} (más antiguo del {i[2]} INC {i[3]})')

            # Salto de línea para separar las zonas
            #print('\n')

            # Imprimir los incidentes para Tolima
            for i in lista_tolima_tr:
                print(f'- {i[0]}: {i[1]} (más antiguo del {i[2]} INC {i[3]})')

        # Obtener el valor de la salida
        inc_tr = output_inc_tr.getvalue()

        # Cerrar la salida de StringIO
        output_inc_tr.close()

        # Mostrar el resultado final (esto se puede descomentar si necesitas ver el resultado)
        #print(inc)
        #print(inc_tr)
        

        #st.markdown(inc)

        #st.markdown(inc_tr)

        st.text(inc)
        st.text("")
        st.text("")
        st.text(inc_tr)



# --------------------- Ingreso de datos WFM ---------------------


    if archivo_datos is not None:

        df_wfm.rename(columns={'Recurso': 'RECURSO'}, inplace=True)
        df_wfm.rename(columns={'Tipo de actividad': 'actividad'}, inplace=True)
        df_wfm = df_wfm.loc[df_wfm['Tipo de actividad.1'].isin(['INCIDENTE-MT', 'INCIDENTE LLAMADA']) & (df_wfm['Estado de actividad']=='pendiente')]
        
        base_path = os.path.expanduser("~")
        
        #df_bol = pd.read_excel('C:\\Users\\gestioncc\\Documents\\proyecto_streamlit\\streamlit-project\\datos\\bol.xlsx')
        ruta = os.path.join(base_path, 'Documents', 'streamlit-project','streamlit-project','datos','bol.xlsx')
  
        df_bol = pd.read_excel(ruta)
        df_bol.rename(columns={'BOL': 'RECURSO'}, inplace=True)
        df_bol['sector'] = df_bol['Mercado'] + ' ' + df_bol['Sector']
        df_bol['sector'] = df_bol['sector'].str.title()
        df = df_wfm.merge(df_bol, how = 'left', on = 'RECURSO')

        lista_ot = df['sector'].value_counts()

        fecha_actual = datetime.now().strftime('%d/%m/%Y')

        fecha_y_hora_actuales = datetime.now()
        zona_horaria = timezone('America/Bogota')
        hora_actual = fecha_y_hora_actuales.astimezone(zona_horaria).strftime('%H:%M')

        lista_ot_it = lista_ot.items()
        sort_list = sorted(lista_ot_it)

        lista_valle_tr_wfm = sorted([i for i in sort_list if 'Valle' in i[0]], key = lambda x: x[0])

        lista_tolima_tr_wfm = sorted([i for i in sort_list if 'Tolima' in i[0]], key = lambda x: x[0])

        output_wfm = io.StringIO()
        with contextlib.redirect_stdout(output_wfm):
            print(f'*Incidentes pendientes BOL en el WFM a las {hora_actual} hrs.*\n')
            for key, value in lista_tolima_tr_wfm:
                print(f'    {key}: {value}')
            print('\n')
            print(f'    *Total Tolima: {sum(i[1] for i in lista_tolima_tr_wfm)}*')
            print('\n')
            for key, value in lista_valle_tr_wfm:
                print(f'    {key}: {value}')
            print('\n')     
            print(f'    *Total Valle: {sum(i[1] for i in lista_valle_tr_wfm)}*')
            print('\n')
            total_ot = sum(lista_ot.to_dict().values())
            print(f'*Total incidentes con corte a las {hora_actual} h del {fecha_actual}: {total_ot}*')


        wfm = output_wfm.getvalue()
        # ------------------------------------------------------------------------------
        # Renombrar CETSA y Pacífico
        wfm = wfm.replace("Valle Cetsa", "CETSA")
        wfm = wfm.replace("Valle Pacifico", "Pacífico")
        # ------------------------------------------------------------------------------
        output_wfm.close()

        st.text(wfm)
