import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from redespacho import mostrar_redespacho
from agc import mostrar_agc,mostrar_agc_unidad
from pruebas import mostrar_pruebas
from ConexionFTP import conexion_ftp, ProcesarDataFTP
from streamlit_autorefresh import st_autorefresh
from dfStyle import tabla_con_estilo, notacion_estilo
from oferta import mostrar_oferta,CargarInformacionOferta

def CargarInformacion(Data, force_reload=False):
    toogle = st.session_state.estado
    if "df" not in st.session_state:
        st.session_state["df"] = pd.DataFrame()
        st.session_state["UltimaCarga"] = datetime.min

    if force_reload:
        print(f"🚀 Cargando FTP para {Data.get('seleccionado')}...")
        conexion_ftp(Data)
        df2 = ProcesarDataFTP(Data)
        st.session_state["df"] = df2
        st.session_state["UltimaCarga"] = datetime.now()
    else:
        df2 = st.session_state["df"]
        print(f"✅ Usando datos cacheados a las {st.session_state['UltimaCarga'].strftime('%H:%M:%S')}")

    return df2

 
def CargarInformacion2(Data,force_reload=False):
    toogle=st.session_state.estado
    if "df" not in st.session_state or "UltimaCarga" not in st.session_state:
        st.session_state["df" ] = pd.DataFrame()
        st.session_state["UltimaCarga" ] = datetime.min

    if  not toogle and force_reload: ## si el toogle está inactivo (no es tiempo real) y se forzó recarga por cambio en el menú, se carga los datos una sola vez
        hora= datetime.now()
        print(f"🚀 Única carga del FTP para {Data.get('seleccionado')}: La carga fue a las {hora.strftime('%d/%m/%Y %H:%M:%S')}.")
        conexion_ftp(Data)
        df2= ProcesarDataFTP(Data)
        st.session_state["df"] = df2
        st.session_state["UltimaCarga"] = hora
    elif Data.get("seleccionado") == "Pruebas" and force_reload: ## si  estamos en pruebas la carga es una sola vez
        hora= datetime.now()
        print(f"🚀 Única carga del FTP para {Data.get('seleccionado')}: La carga fue a las {hora.strftime('%d/%m/%Y %H:%M:%S')}.")
        conexion_ftp(Data)
        df2= ProcesarDataFTP(Data)
        st.session_state["df"] = df2
        st.session_state["UltimaCarga"] = hora
    elif (force_reload or datetime.now() - st.session_state["UltimaCarga"] > timedelta(seconds=intervalo))and Data.get("seleccionado") != "Pruebas" and toogle:
        print(f"🚀 Iniciando recarga del FTP: Última carga fue hace más de {intervalo/60} minutos.")
        conexion_ftp(Data)
        df2= ProcesarDataFTP(Data)
        st.session_state["df"] = df2
        st.session_state["UltimaCarga"] = datetime.now()
        print(f"📥 Datos recargados del FTP a las {st.session_state['UltimaCarga'].strftime('%H:%M:%S')}")
    else:
        df2 = st.session_state["df"]
        print(f"✅ Usando datos cacheados a las {st.session_state['UltimaCarga'].strftime('%H:%M:%S')}")

    return df2

def ProcesarInformacion(df2, Data):
    if Data["error"]["Bandera"]:
        st.error(f"Error al cargar los datos: {Data['error']['Mensaje']}")
        return
    elif df2.shape[0]==0:
        st.warning(f"No hay datos para {Data['seleccionado']}")
        return
    if st.session_state.pagina_actual=="Oferta":
        return

    fila_a_marcar = int(datetime.now().hour+0) if st.session_state.estado else -1 
    # Mostrar la tabla
    tabla_html= tabla_con_estilo(df2, fila_a_marcar)
    #st.markdown(tabla_html,unsafe_allow_html=True)

    # Mostrar todo en componente HTML
    with open("estilos.css") as f:
        custom_css=f"<style>{f.read()}</style>"
  
    with open("scripts.js", "r") as f:
        js_script = f"<script>{f.read()}</script>"

    if st.session_state.get("transponer",True):
        Ncolumnas=df2.shape[0]+1
        Nfilas=df2.shape[1]+1
    else:
        Ncolumnas=df2.shape[1]+1
        Nfilas=df2.shape[0]+1  
    st.components.v1.html(f"""
    {custom_css}
    {tabla_html}
    {js_script}
    """,height=40*Nfilas,width=3000,scrolling=True)
    if Data["seleccionado"] == "Pruebas":
        texto=notacion_estilo(Data["Notacion"])
        st.markdown(texto, unsafe_allow_html=True)


TIEMPO_ACTUALIZACION_MINUTOS = 5
TIEMPO_LECTURA_FTP = 2*TIEMPO_ACTUALIZACION_MINUTOS
intervalo = TIEMPO_LECTURA_FTP * 60              # en segundos (para comparación de timestamps)
vinterval = TIEMPO_ACTUALIZACION_MINUTOS * 60_000           # en milisegundos (para st_autorefresh)
# Rerun cada 60 segundos (opcional, puedes ajustarlo)
now = datetime.now()
minutes = now.minute
seconds = now.second
# Próximo múltiplo de 5 minutos
next_interval_minute = (minutes // TIEMPO_ACTUALIZACION_MINUTOS + 1) * TIEMPO_ACTUALIZACION_MINUTOS
if next_interval_minute >= 60:
    next_time = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
else:
    next_time = now.replace(minute=next_interval_minute, second=0, microsecond=0)

# Calcular milisegundos hasta el próximo múltiplo de 5 minutos
delta = (next_time - now).total_seconds() * 1000
interval_ms = int(delta)

# Iniciar el refresco con el tiempo exacto restante
st_autorefresh(interval=interval_ms, key="precise_refresh")


# Función principal de Streamlit
def DetectarCambio(origen):
    # Si el cambio vino del toggle ("toogle") y fue activado, forzamos la fecha de hoy
    if origen == "toogle":
        if st.session_state.estado:
            st.session_state["FechaSeleccionada"] = datetime.today().date()
            st.session_state["CambioDetectado"] = True
    # si el cambio vino del selector de fecha y la feha seleccionada es diferente a la fecha actualmente seleccionada, fozamos el cambio    
    if origen == "SeleccionFecha": 
        if st.session_state.FechaSeleccionada != st.session_state.FechaSeleccionada2:
            st.session_state["CambioDetectado"] = True
    if origen == "transponer":
        # Si se presiona el botón de transponer, forzamos el cambio
        st.session_state["CambioDetectado"] = True 
        st.session_state["transponer"] = not st.session_state.get("transponer", True)  # Alternar el estado de transposición
              
def IncializarVariablesSesion():
    if "CambioDetectado" not in st.session_state:
        st.session_state["CambioDetectado"]=False
    if "FechaSeleccionada2" not in st.session_state:
        st.session_state["FechaSeleccionada2"]=datetime.today()
    if "FechaActual" not in st.session_state:
        st.session_state["FechaActual"]=st.session_state["FechaSeleccionada2"]
    if "transponer" not in st.session_state:
        st.session_state["transponer"] = True
    if "pagina_actual" not in st.session_state:
        st.session_state.pagina_actual = ""
    if "UltimaCarga" not in st.session_state:   
        st.session_state["UltimaCarga"] = datetime.now() - timedelta(days=1)  # Inicializar con una fecha pasada para forzar la carga inicial 
def app():
    with open("estilos.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
  
 #   with open("scripts.js", "r") as f:
#        js_script = f.read()
 #       st.components.v1.html(f"<script>{js_script}</script>", height=0, width=0)
    st.title("Redespacho-Conexión al FTP")
    IncializarVariablesSesion()

    col1,col2,col3 = st.columns(3)
    with col2:
        st.write("tiempo real o historico")
        # Crear mensaje dinámico en base al valor actual
        mensaje_dinamico = "🟢 Hoy" if st.session_state.get("estado", True) else "🔴 Histórico"
        # Toggle que puede cambiar la fecha si se activa
        activarfecha = st.toggle(
            mensaje_dinamico,
            key="estado",
            value=st.session_state.get("estado", True),
            on_change=DetectarCambio,
            args=("toogle",)
        )
        st.session_state["estadoactual"]=activarfecha
        # Detectar cambio de día y en caso de ser así, forzar la fecha de hoy
         
    with col1:    
        if st.session_state.FechaActual != datetime.today().date():
            st.session_state["FechaSeleccionada"]=datetime.today().date()
            st.session_state["FechaActual"]=st.session_state["FechaSeleccionada"]
            st.session_state["CambioDetectado"] = True
        # Mostrar selector de fecha (deshabilitado si el toggle está activado)
        fecha = st.date_input(
            "Selecciona una fecha",
            key="FechaSeleccionada",
            disabled=activarfecha,
            max_value=datetime.today().date()+timedelta(days=1),
            on_change=DetectarCambio,
            args=("SeleccionFecha",)
        )
        
    # Detectar si hubo cambio en la fecha
    cambio_fecha = st.session_state.FechaSeleccionada != st.session_state.FechaSeleccionada2

    st.session_state["FechaSeleccionada2"] = fecha
 # Menú de selección
    seleccion = st.selectbox(
    "Seleccione una opción",
    ("Redespacho", "AGC", "AGC Unidad","Pruebas","Oferta"))

    # Detectar si hubo cambio en la página
    cambio_pagina = seleccion != st.session_state.pagina_actual
        # Para modo histórico (toggle OFF), recarga solo si cambio fecha o página
    # (si quieres que también recargue si cambia página, si no, solo cambio fecha)
    if not st.session_state.estado:
        recarga_tiempo=False
    else:
        # En modo tiempo real (toggle ON), recarga si pasó el intervalo o cambio página
        recarga_tiempo = datetime.now() - st.session_state["UltimaCarga"] > timedelta(seconds=intervalo)
    
    Recargar = cambio_fecha or cambio_pagina or recarga_tiempo or cambio_pagina
    
    #Recargar = seleccion != st.session_state.pagina_actual or st.session_state["CambioDetectado"]
    st.session_state.pagina_actual = seleccion  # actualizar la página actual
 # Mostrar el contenido según la opción seleccionada
    if seleccion == "Redespacho":
        Data=mostrar_redespacho(fecha)
    elif seleccion == "AGC":
        Data= mostrar_agc(fecha)
    elif seleccion == "AGC Unidad":
        Data= mostrar_agc_unidad(fecha)    
    elif seleccion == "Pruebas":
        Data=mostrar_pruebas(fecha)
    elif seleccion=="Oferta":
        Data=mostrar_oferta(fecha)   
    # Cargamos los datos del FTP o del caché según el intervalo de tiempo definido o el tipo de selección
    if seleccion!="Oferta":
        df2=CargarInformacion(Data,force_reload=Recargar)
    else:
        df2=CargarInformacionOferta(Data,force_reload=Recargar)    
    horaderecarga = datetime.now()
    print(f"📥 Datos recargados a las {st.session_state['UltimaCarga'] .strftime('%H:%M:%S')}")
    with col3:
        st.write("última carga del FTP: ",st.session_state['UltimaCarga'] .strftime('%H:%M:%S'))
        st.write("última recarga de la página: ",horaderecarga.strftime('%H:%M:%S'))
    # agregar boton para trasponer la tabla
    if seleccion !="Oferta":
        st.button("cambiar vista", on_click=DetectarCambio, args=("transponer",))
    ProcesarInformacion(df2,Data)

    st.session_state["CambioDetectado"]=False
# Ejecutar la aplicación Streamlit
if __name__ == '__main__':
    app()
