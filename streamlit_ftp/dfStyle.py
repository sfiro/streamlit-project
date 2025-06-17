import streamlit as st
# Convertir el DataFrame a HTML
def tabla_con_estilo(df, fila_resaltada):
    if st.session_state.get("transponer",False):
        df=df.T.reset_index()  # Transponer el DataFrame para que las columnas sean las filas y viceversa
        new_header = df.iloc[0].copy()  # Guardar la primera fila como encabezado
        new_header.iloc[0]='Unidad o Planta'
        df=df[1:]
        df.columns = new_header  # Asignar la primera fila como encabezado
    
    html = """
        <style>
        .table-wrapper, .table-container, table {
            background-color: #18191A !important;
            color: #F5F6FA !important;
        }
        th, td {
            background-color: #18191A !important;
            color: #F5F6FA !important;
            border: 1px solid #444 !important;
        }
        .resaltado {
            background-color: #D5752D !important;
            color: #fff !important;
        }
        </style>
        """
    html += '<div class="table-wrapper"><div class="table-container"><table>'
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
    html = """
        <style>
        .notas {
            background-color: #18191A !important;
            color: #F5F6FA !important;
            border-radius: 8px;
            padding: 16px;
            margin-top: 12px;
            margin-bottom: 12px;
        }
        .notas ul {
            color: #F5F6FA !important;
        }
        .notas li {
            margin-bottom: 6px;
        }
        .notas strong, .notas span {
            color: #D5752D !important;
        }
        </style>
        
    """
    for key, dato in data.items():
        if key == "":
            key = "''"
        html += f'<li><span> {key}</span>: {dato}</li>'
    html += """
            </ul>
        </div>
    """
    return html
