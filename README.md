# Streamlit Project

Este proyecto es una aplicación interactiva desarrollada con [Streamlit](https://streamlit.io/), diseñada para visualizar y analizar datos relacionados con consignaciones, incidentes y métricas de SAIDI. La aplicación incluye gráficos dinámicos, métricas clave y una interfaz amigable para el usuario.

## Características

- **Visualización de datos**:
  - Gráficos de torta y barras para analizar consignaciones por zona.
  - Métricas clave como el número total de consignaciones, incidentes y SAIDI.
  - Tablas interactivas para explorar los datos.

- **Interfaz dinámica**:
  - Barra lateral con opciones de navegación.
  - Actualización automática de datos cada 60 segundos.
  - Animaciones Lottie para mejorar la experiencia visual.

- **Datos procesados**:
  - Consignaciones agrupadas por subestaciones.
  - Incidentes agrupados por subregiones.
  - Métricas de SAIDI.

## Requisitos previos

Asegúrate de tener instalados los siguientes componentes:

- Python 3.8 o superior
- [Streamlit](https://streamlit.io/)
- Bibliotecas adicionales:
  - `pandas`
  - `plotly`
  - `altair`
  - `requests`
  - `streamlit-lottie`

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/sfiro/streamlit-project.git
   cd streamlit-project
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación:
   ```bash
   streamlit run Dashboard.py
   ```

2. Abre tu navegador en la dirección que aparece en la terminal (por defecto, [http://localhost:8501](http://localhost:8501)).

3. Navega por las diferentes secciones de la barra lateral:
   - **Resumen**: Métricas generales de consignaciones, incidentes y SAIDI.
   - **Consignaciones**: Visualización de consignaciones por zona.
   - **Incidentes**: Análisis de incidentes por subregión.
   - **SAIDI**: Métricas relacionadas con SAIDI.
   - **Entrega turno**: Información adicional sobre la entrega de turnos.

## Estructura del proyecto

```
streamlit-project/
├── Dashboard.py           # Archivo principal de la aplicación
├── consignaciones.py      # Módulo para la sección de consignaciones
├── incidentes.py          # Módulo para la sección de incidentes
├── resumenApp2.py         # Módulo para la sección de resumen
├── datos/                 # Carpeta con los archivos de datos
│   ├── Consignaciones.csv
│   ├── IncidentesActual.csv
│   └── SAIDIPendientes.csv
├── logo/                  # Carpeta con el logo del proyecto
│   └── logoCelsia.png
├── estilo.css             # Archivo de estilos personalizados
├── README.md              # Documentación del proyecto
└── requirements.txt       # Lista de dependencias
```

## Personalización

- **Logo**: Puedes cambiar el logo ubicado en `logo/logoCelsia.png` por el de tu organización.
- **Datos**: Asegúrate de que los archivos de datos en la carpeta `datos/` estén actualizados y sigan el formato esperado.
- **Estilos**: Puedes personalizar los estilos de la aplicación modificando el archivo `estilo.css`.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.