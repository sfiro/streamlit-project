from ftplib import FTP_TLS
import pandas as pd
from io import BytesIO
import os
import sys
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

host = "xmftps.xm.com.co"  # Reemplaza con el host real
#archivo="rDec0504.txt"
archivo_entrada="Despacho.xlsm"
#carpeta="2025-05"
plantas_interes = ['ALBAN', 'CALIMA', 'SALVAJINA','PRADO','CUCUANA','MERILECTRICA 1','TESORITO']
Unidades_interes=['ALTO ANCHICAYA','BAJO ANCHICAYA','CALIMA','PRADO','CUCUANA','MERILECTRICA 1','TESORITO']
plantas_interes=[aux.replace(' ', '') for aux in plantas_interes]
Plantas=["Alban","Calima","Salvajina","Prado","Cucuana","Merilectrica","Tesorito"]
diccionario = dict(zip(plantas_interes, Plantas))
def ProcesarDataPalanta(Data):
    contenido = Data["contenidoFTP"]
    datos=[["Period"]+[str(i) for i in range(1, 25)]]
    for unidad in Unidades_interes:
        for linea in contenido:
            
            if not unidad in linea:
                continue
            partes=linea.replace('"', '').split(',')
            valores=list(map(str,partes))
            datos.append(valores)
    if len(datos) >1:
        df2=pd.DataFrame(datos)
        df2=df2.T
        new_header = df2.iloc[0].copy()
        df2.columns = new_header  # Asignar la primera fila como encabezado
        df2 = df2[1:]  # Eliminar la primera fila que ahora es el encabezado
        #columnas=['unidad']+[str(i) for i in range(1, len(datos[0]))]
        #df=pd.DataFrame(datos,columns=columnas)
        df=df2
    else:    
        df=pd.DataFrame()
    return df

def loggingFTP(usuario,contra):
    ftp = FTP_TLS()
    ftp.connect(host=host, port=210)
    ftp.login(user=usuario, passwd=contra)
    ftp.prot_p()  # Activa cifrado para canal de datos
    return ftp

def conexion_ftp(Data):

    usuario = os.getenv("FTP_USER1")
    contra = os.getenv("FTP_PASS1")
    usuario2 = os.getenv("FTP_USER2")
    contra2 = os.getenv("FTP_PASS2")
    ruta=Data["ruta"]
    archivo=Data["archivo"]

    try:
        # Conexión FTPS
        ftp = loggingFTP(usuario,contra)
    except Exception as e:
        print(f"Error al conectar con el usuario 1: {e}")
        ftp = None
        try:
            if not ftp:
                # Si falla la conexión, intenta con otro usuario
                ftp = loggingFTP(usuario2,contra2)
        except Exception as e:
            print(f"Error al conectar con el usuario 2: {e}")
            ftp = None
            Data["contenidoFTP"]=[]
            Data['error']['Mensaje'] = "No se pudo conectar al servidor FTP con ninguno de los usuarios."
            Data["error"]["Bandera"] = True
            return
    try:
        # Cambia al directorio deseado
        ftp.cwd('/INFORMACION_XM/PUBLICO/'+ruta+'/')
        buffer = BytesIO()
        ftp.retrbinary('RETR '+archivo, buffer.write)
        # Procesa el contenido (decodifica si es texto)
        contenido = buffer.getvalue().decode('utf-8').splitlines()
    except Exception as e:
        print(f"Error al recuperar el archivo {archivo} en la carpeta {ruta}: {e}")
        contenido = []
        Data['error']['Mensaje'] = "No se pudo conectar a la ruta especificada, intentelo más tarde"
        Data['error']['Bandera'] = True
    finally:    
        ftp.quit()
	    ## Depurando el contenido
        Data["contenidoFTP"]=contenido

def ProcesarDataFTP(Data):
    datos = {}
    if Data["seleccionado"]=="Pruebas" or Data["seleccionado"]=="AGC_Unidad":
        df=ProcesarDataPalanta(Data)
        return df
    contenido = Data["contenidoFTP"]
    for linea in contenido:
        partes = linea.replace('"', '')
        partes = partes.replace(' ', '')
        partes=partes.split(',')
        nombre_planta = partes[0]
        if nombre_planta not in plantas_interes:
            continue
        valores = list(map(float, partes[1:]))
        datos[diccionario[nombre_planta]] = valores
		
        # validar si datos es vacio y crear dataframe
    if not datos:
        print("No se encontraron datos para las plantas de interés.")
        df=pd.DataFrame()
    else: # se crea el dataframe con contenido de datos
        df = pd.DataFrame(datos)
        if len(datos)>=len(Plantas):
            df = df[Plantas]
        df.insert(0, 'Periodo', range(1, 25))  # Periodos del 1 al 24
        print(df)
    
    return df
