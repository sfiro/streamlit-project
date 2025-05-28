import streamlit as st
import pandas as pd
import plotly.express as px
import pandas as pd
<<<<<<< HEAD
from datetime import datetime
from pytz import timezone
import io
import contextlib
=======
>>>>>>> e2257ca0d9d71bbe42890ae09dd74379d30903aa

def gestion():
    
    st.title('Datos de ingreso')
    
    archivo_datos = st.file_uploader("subir CSV", type=["csv", "xlsx"])
    if archivo_datos is not None:
        try:
            detalle_archivo = {
                "Nombre del archivo": archivo_datos.name,
                "Tipo de archivo": archivo_datos.type,
                "Tamaño del archivo": archivo_datos.size
            }
            #st.write(detalle_archivo)

            if detalle_archivo["Tipo de archivo"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
<<<<<<< HEAD
                df_incidentes = pd.read_excel(archivo_datos, engine="openpyxl")
            elif detalle_archivo["Tipo de archivo"] == "text/csv":
                df_incidentes = pd.read_csv(archivo_datos, sep=';', skiprows=3)
=======
                datos = pd.read_excel(archivo_datos, engine="openpyxl")
            elif detalle_archivo["Tipo de archivo"] == "text/csv":
                datos = pd.read_csv(archivo_datos, sep=';', skiprows=3)
>>>>>>> e2257ca0d9d71bbe42890ae09dd74379d30903aa
            else:
                st.error("Formato de archivo no soportado.")
                return

<<<<<<< HEAD
            if df_incidentes.empty:
                st.warning("El archivo cargado está vacío.")
                return

            st.dataframe(df_incidentes)
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
                print(f'*Con corte en el sistema ADMS a las {hora_actual}, tenemos {sum(lista_incidentes.values)} incidentes pendientes mtto.*\n')

                # Imprimir los incidentes para Valle, solo el más antiguo por sector
                print(f'*Para Valle tenemos {total_valle} pendientes mtto, distribuidos por sector así:*\n')
                for i in lista_valle:
                    print(f'{i[0]}: {i[1]} (más antiguo del {i[2]} INC {i[3]} - {i[4]})\n')
                print('\n')
                # Imprimir los incidentes para Tolima, solo el más antiguo por sector
                print(f'*Para Tolima tenemos {total_tolima} pendientes mtto, distribuidos por sector así:*\n')
                for i in lista_tolima:
                    print(f'{i[0]}: {i[1]} (más antiguo del {i[2]} INC {i[3]} - {i[4]})\n')

            # Obtener el valor del output generado
            inc = output_inc.getvalue()

            # ------------------------------------------------------------------------------
            # Renombrar CETSA y Pacífico
            inc = output_inc.getvalue()
            inc = inc.replace("Valle Cetsa", "CETSA")
            inc = inc.replace("Valle Pacifico", "Pacífico")
            # ------------------------------------------------------------------------------
            output_inc.close()




=======
            if datos.empty:
                st.warning("El archivo cargado está vacío.")
                return

            st.dataframe(datos)
>>>>>>> e2257ca0d9d71bbe42890ae09dd74379d30903aa

        except Exception as e:
            st.error(f"Error al procesar el archivo: {e}")
    
<<<<<<< HEAD
=======
    # Eliminar los excluibles
    df_incidentes = df_incidentes[~df_incidentes['Causa'].str.startswith('Exc_')]
>>>>>>> e2257ca0d9d71bbe42890ae09dd74379d30903aa
