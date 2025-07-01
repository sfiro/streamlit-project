import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from redespacho import mostrar_redespacho, mostrar_despacho
from agc import mostrar_agc,mostrar_agc_unidad
from pruebas import mostrar_pruebas
from ConexionFTP import conexion_ftp, ProcesarDataFTP
from streamlit_autorefresh import st_autorefresh
from dfStyle import tabla_con_estilo, notacion_estilo
from oferta import mostrar_oferta,CargarInformacionOferta
import plotly.express as px
import plotly.graph_objects as go

def CargarInformacion(Data, force_reload=False):
    """Carga los datos desde el FTP o desde caché, según corresponda."""
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
    """Carga los datos desde el FTP o caché, considerando el modo histórico o tiempo real."""
    toogle=st.session_state.estado
    if "df" not in st.session_state or "UltimaCarga" not in st.session_state:
        st.session_state["df" ] = pd.DataFrame()
        st.session_state["UltimaCarga" ] = datetime.min

    if  not toogle and force_reload:  # Carga única si está en modo histórico y se forza recarga
        hora= datetime.now()
        print(f"🚀 Única carga del FTP para {Data.get('seleccionado')}: La carga fue a las {hora.strftime('%d/%m/%Y %H:%M:%S')}.")
        conexion_ftp(Data)
        df2= ProcesarDataFTP(Data)
        st.session_state["df"] = df2
        st.session_state["UltimaCarga"] = hora
    elif Data.get("seleccionado") == "Pruebas" and force_reload:  # Carga única para pruebas
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
    """Procesa y muestra la información en la tabla, aplica estilos y muestra advertencias o errores si corresponde."""
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
        st
        st.markdown(texto, unsafe_allow_html=True)



def DetectarCambio(origen):
    """Detecta cambios en el estado de la página (toggle, fecha, transponer) y actualiza las variables de sesión."""
    if origen == "toogle":
        if st.session_state.estado:
            st.session_state["FechaSeleccionada"] = datetime.today().date()
            st.session_state["CambioDetectado"] = True
    if origen == "SeleccionFecha": 
        if st.session_state.FechaSeleccionada != st.session_state.FechaSeleccionada2:
            st.session_state["CambioDetectado"] = True
    if origen == "transponer":
        st.session_state["CambioDetectado"] = True 
        st.session_state["transponer"] = not st.session_state.get("transponer", True)  # Alternar el estado de transposición
              
def IncializarVariablesSesion():
    """Inicializa las variables necesarias en la sesión de Streamlit."""
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
    """Función principal de la aplicación Streamlit: controla la interfaz, navegación y recarga de datos."""
    with open("estilos.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
  
    st.title("Redespacho-Conexión al FTP")
    IncializarVariablesSesion()

    col1,col2,col3 = st.columns(3)
    with col2:
        st.write("tiempo real o historico")
        mensaje_dinamico = "🟢 Hoy" if st.session_state.get("estado", True) else "🔴 Histórico o Futuro"
        activarfecha = st.toggle(
            mensaje_dinamico,
            key="estado",
            value=st.session_state.get("estado", True),
            on_change=DetectarCambio,
            args=("toogle",)
        )
        st.session_state["estadoactual"]=activarfecha
         
    with col1:    
        if st.session_state.FechaActual != datetime.today().date():
            st.session_state["FechaSeleccionada"]=datetime.today().date()
            st.session_state["FechaActual"]=st.session_state["FechaSeleccionada"]
            st.session_state["CambioDetectado"] = True
        fecha = st.date_input(
            "Selecciona una fecha",
            key="FechaSeleccionada",
            disabled=activarfecha,
            max_value=datetime.today().date()+timedelta(days=1),
            on_change=DetectarCambio,
            args=("SeleccionFecha",)
        )
        
    cambio_fecha = st.session_state.FechaSeleccionada != st.session_state.FechaSeleccionada2
    st.session_state["FechaSeleccionada2"] = fecha

    seleccion = st.selectbox(
        "Seleccione una opción",
        ("Redespacho", "AGC", "AGC Unidad","Pruebas","Oferta"))

    cambio_pagina = seleccion != st.session_state.pagina_actual
    if not st.session_state.estado:
        recarga_tiempo=False
    else:
        recarga_tiempo = datetime.now() - st.session_state["UltimaCarga"] > timedelta(seconds=intervalo)
    
    Recargar = cambio_fecha or cambio_pagina or recarga_tiempo or cambio_pagina
    st.session_state.pagina_actual = seleccion  # actualizar la página actual

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

    if seleccion!="Oferta":
        df_redespacho=CargarInformacion(Data,force_reload=True)
        ProcesarInformacion(df_redespacho,Data)
    else:
        df_oferta=CargarInformacionOferta(Data,force_reload=True)
        ProcesarInformacion(df_oferta,Data)

    horaderecarga = datetime.now()
    print(f"📥 Datos recargados a las {st.session_state['UltimaCarga'] .strftime('%H:%M:%S')}")
    with col3:
        st.write("última carga del FTP: ",st.session_state['UltimaCarga'] .strftime('%H:%M:%S'))
        st.write("última recarga de la página: ",horaderecarga.strftime('%H:%M:%S'))


    if seleccion !="Oferta":
        st.button("cambiar vista", on_click=DetectarCambio, args=("transponer",))

    

    if seleccion == "Redespacho":
        Data2 = mostrar_despacho(fecha)
        df_despacho=CargarInformacion(Data2,force_reload=True)
        #st.dataframe(df_despacho)
        selectorPlantas(df_despacho,df_redespacho)

         

    elif seleccion == "AGC":
        Data2 = mostrar_agc(fecha)
        df_despacho=CargarInformacion(Data2,force_reload=True)
        #st.write(Data2)
        #st.dataframe(df_despacho)
        selectorPlantas(df_despacho,df_redespacho)



    

    st.session_state["CambioDetectado"]=False

# Configuración de refresco automático
TIEMPO_ACTUALIZACION_MINUTOS = 5
TIEMPO_LECTURA_FTP = 2*TIEMPO_ACTUALIZACION_MINUTOS
intervalo = TIEMPO_LECTURA_FTP * 60              # en segundos (para comparación de timestamps)
vinterval = TIEMPO_ACTUALIZACION_MINUTOS * 60_000           # en milisegundos (para st_autorefresh)
now = datetime.now()
minutes = now.minute
seconds = now.second
next_interval_minute = (minutes // TIEMPO_ACTUALIZACION_MINUTOS + 1) * TIEMPO_ACTUALIZACION_MINUTOS
if next_interval_minute >= 60:
    next_time = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
else:
    next_time = now.replace(minute=next_interval_minute, second=0, microsecond=0)
# delta = (next_time - now).total_seconds() * 1000
# interval_ms = int(delta)
# st_autorefresh(interval=interval_ms, key="precise_refresh")

# Ejecutar la aplicación Streamlit
if __name__ == '__main__':
    count = st_autorefresh(interval=60000, limit=100, key="ftp_autorefresh")
    app()

def selectorPlantas(despacho,redespacho):
    seleccion = st.selectbox(
        "Seleccione una opción",
        ("Alban", "Calima", "Salvajina","Prado","Cucuana","Merilectrica","Tesorito"))

    if seleccion == "Alban":
        barras(despacho,redespacho, "Alban",key = "Generación barras"+seleccion)
    elif seleccion == "Calima":
        barras(despacho,redespacho, "Calima",key = "Generación barras"+seleccion)
    elif seleccion == "Salvajina":
        barras(despacho,redespacho, "Salvajina",key = "Generación barras"+seleccion) 
    elif seleccion == "Prado":
        barras(despacho,redespacho, "Prado",key = "Generación barras"+seleccion)
    elif seleccion=="Cucuana":
        barras(despacho,redespacho, "Cucuana",key = "Generación barras"+seleccion)
    elif seleccion=="Merilectrica":
        barras(despacho,redespacho, "Merilectrica",key = "Generación barras"+seleccion)  
    elif seleccion=="Tesorito":
        barras(despacho,redespacho, "Tesorito",key = "Generación barras"+seleccion)   


def barras(despacho,redespacho,planta,key = "Generación Alban"):

    # Verificar que la planta existe en ambos DataFrames y tiene datos
    if planta not in despacho.columns or planta not in redespacho.columns:
        st.warning(f"La planta '{planta}' no existe en los datos.")
        return
    if despacho[planta].dropna().empty or redespacho[planta].dropna().empty:
        st.warning(f"No hay datos para la planta '{planta}'.")
        return
    
    redespacho[planta] = redespacho[planta].replace(0, 0.01)
    despacho[planta] = despacho[planta].replace(0, 0.01)
    
    fig_bar = go.Figure()

    # Primera barra (df2)
    fig_bar.add_bar(
        x=redespacho['Periodo'],
        y=redespacho[planta],
        name='reDespacho' + planta,
        text=redespacho[planta].round(0).astype(int),            # <-- Muestra el valor sobre la barra
        textposition='outside'              # <-- Posición del texto
    )

    # Segunda barra (df3)
    fig_bar.add_bar(
        x=despacho['Periodo'],
        y=despacho[planta],
        name='Despacho' + planta,
        text=despacho[planta].round(0).astype(int),            # <-- Muestra el valor sobre la barra
        textposition='outside'              # <-- Posición del texto
    )

    fig_bar.update_layout(
        title="Despacho " + planta + "Comparativo",
        barmode='group'  # Usa 'stack' para apilar, 'group' para barras lado a lado
    )
    fig_bar.update_xaxes(type='category', tickangle=0)  # <-- Fuerza mostrar todos los índices


    st.plotly_chart(fig_bar,key = key)

def lineas(despacho,redespacho,planta = "Alban",key = "Generación Alban"):
    fig_line = go.Figure()

    # Primera línea (df2)
    fig_line.add_trace(go.Scatter(
        x=redespacho['Periodo'],
        y=redespacho[planta],
        mode='lines+markers',
        name='reDespacho' + planta
    ))

    # Segunda línea (df3)
    fig_line.add_trace(go.Scatter(
        x=despacho['Periodo'],
        y=despacho[planta],
        mode='lines+markers',
        name='Despacho' + planta
    ))

    fig_line.update_layout(
        title="Despacho " + planta + "Comparativo",
        xaxis_title="Periodo",
        yaxis_title= planta
    )

    st.plotly_chart(fig_line, key=key)

def area(despacho,redespacho,planta = "Alban",key = "Generación Alban"):
    fig_area = go.Figure()

    # Primera área (df2)
    fig_area.add_trace(go.Scatter(
        x=redespacho['Periodo'],
        y=redespacho[planta],
        mode='lines',
        name='reDespacho ' + planta,
        stackgroup='one',  # Agrupa para apilar
        line=dict(width=0.5),
        marker=dict(size=4)
    ))

    # Segunda área (df3)
    fig_area.add_trace(go.Scatter(
        x=despacho['Periodo'],
        y=despacho[planta],
        mode='lines',
        name='Despacho '+ planta,
        stackgroup='Two',  # Mismo grupo para apilar
        line=dict(width=2, color='#FFA500'),  # Naranja
        marker=dict(size=4)
    ))

    fig_area.update_layout(
        title="Despacho " + planta + " Comparativo",
        xaxis_title="Periodo",
        yaxis_title=planta,
        showlegend=True
    )

    st.plotly_chart(fig_area, key=key)