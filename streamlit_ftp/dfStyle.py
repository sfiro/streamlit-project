
# Importar Streamlit para usar variables de sesión y mostrar componentes
import streamlit as st
# Convertir el DataFrame a HTML con estilos personalizados y resaltado de diferencias

def tabla_con_estilo(df, fila_resaltada, df_diff):

    # Si la opción de transponer está activada, transpone el DataFrame y ajusta encabezados
    #st.dataframe(df_diff)
    if st.session_state.get("transponer", False):
        
        df = df.T.reset_index()  # Transponer el DataFrame para que las columnas sean las filas y viceversa
        new_header = df.iloc[0].copy()  # Guardar la primera fila como encabezado
        new_header.iloc[0] = 'Unidad o Planta'  # Cambiar el nombre de la primera columna
        df = df[1:]
        df.columns = new_header  # Asignar la primera fila como encabezado

        df_diff = df_diff.T.reset_index() 
        df_diff = df_diff[1:]
        df_diff.columns = new_header  # Asignar la primera fila como encabezado

    else:
        pass


    
    # Definir los estilos CSS para la tabla y las clases de resaltado
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
        .diferente {
            background-color: #FF3B30 !important;
            color: #fff !important;
        }
        </style>
        """
    # Iniciar la tabla HTML
    html += '<div class="table-wrapper"><div class="table-container"><table>'
    html += '<table>'
    # Encabezados de la tabla
    html += '<thead><tr>' + ''.join(
        f'<th>{int(col) if not isinstance(col, str) else col}</th>' 
        for col in df.columns
    ) + '</tr></thead>'
    # Cuerpo de la tabla
    html += '<tbody>'
    for i, row in df.iterrows():
        #st.write("fila =",i)
        html += f'<tr>'
        for columname, val in row.items():
            #st.write("column = ",columname)
            # Si la columna es 'Periodo', mostrar como entero sin decimales
            if columname == 'Periodo':
                aux = format(int(val), '#d')
            else:
                aux = val

            # Determinar si hay diferencia en este valor usando df_diff
            clase = ''
            if df_diff is not None:

                diff_val = df_diff.at[row.name, columname] if columname in df_diff.columns else 0
                if diff_val == 1:
                    #st.write("fila =",i)
                    #st.write("column = ",columname)
                    clase = 'diferente'  # Resalta en rojo si hay diferencia
                #st.write("diff_val =",diff_val)
            
            # Resaltado de fila seleccionada
            if i == fila_resaltada and not st.session_state.get("transponer", False):
                clase = 'resaltado' if clase == '' else clase
            elif columname == fila_resaltada+1 and st.session_state.get("transponer", False):
                clase = 'resaltado' if clase == '' else clase
            # Agregar la celda con la clase correspondiente
            html += f'<td class="{clase}">{aux}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    html += '</table></div></div>'
    return html

def notacion_estilo(data):
    # Genera HTML para mostrar anotaciones con estilo personalizado
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
