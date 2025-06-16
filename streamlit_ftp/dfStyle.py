import streamlit as st
# Convertir el DataFrame a HTML
def tabla_con_estilo(df, fila_resaltada):
    if st.session_state.get("transponer",False):
        df=df.T.reset_index()  # Transponer el DataFrame para que las columnas sean las filas y viceversa
        new_header = df.iloc[0].copy()  # Guardar la primera fila como encabezado
        new_header.iloc[0]='Unidad o Planta'
        df=df[1:]
        df.columns = new_header  # Asignar la primera fila como encabezado
    
    html = '<div class="table-wrapper"><div class="table-container"><table>'
    html += '<table>'
    # Encabezados
    html += '<thead><tr>' + ''.join(
    f'<th>{int(col) if not isinstance(col, str) else col}</th>' 
    for col in df.columns
    ) + '</tr></thead>'
    # Cuerpo
    html += '<tbody>'
    for i, row in df.iterrows():
        
        html += f'<tr>' 
        for columname,val in row.items():
            if columname=='Periodo':
                # aplicar formato de quitar decimales
                aux= format(int(val),'#d')
            else:
                aux=val 
            if i == fila_resaltada and not st.session_state.get("transponer",False):
                clase = 'resaltado' 
            elif columname == fila_resaltada+1 and st.session_state.get("transponer",False): 
                clase = 'resaltado' 
            else:    
                clase = '' 
            html+=f'<td class="{clase}">{aux}</td>'
        html+= '</tr>'
    html += '</tbody></table>'
    html += '</table></div></div>'
    return  html
def notacion_estilo(data):
    html=    """
        <div class="notas">
            <p><span><strong>Notación:</strong></span></p>
            <ul>"""
    for key,dato in data.items():
        if key=="":
            key="''"
        html+=f'<li><span> {key}</span>: {dato}</li> ' 
    html+="""
            </ul>
        </div>
        """
    return html
    