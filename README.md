# Streamlit Project

Este proyecto es una aplicación interactiva desarrollada con [Streamlit](https://streamlit.io/), diseñada para visualizar y analizar datos relacionados con consignaciones, incidentes y métricas de SAIDI. La aplicación incluye gráficos dinámicos, métricas clave y una interfaz amigable para el usuario.

## Características

- **Visualización de datos**:
  - Gráficos de torta, barras, radar y donut para analizar consignaciones e incidentes por zona y subregión.
  - Métricas clave como el número total de consignaciones, incidentes y SAIDI.
  - Tablas interactivas para explorar los datos.

- **Interfaz dinámica**:
  - Barra lateral con navegación por secciones.
  - Actualización automática de datos.
  - Animaciones Lottie para una mejor experiencia visual.

- **Procesamiento de datos**:
  - Consignaciones agrupadas por subestaciones.
  - Incidentes agrupados por subregiones y estados.
  - Métricas y reportes de SAIDI.

## Requisitos previos

Asegúrate de tener instalado:

- Python 3.8 o superior
- [Streamlit](https://streamlit.io/)
- Bibliotecas adicionales:
  - `pandas`
  - `plotly`
  - `altair`
  - `requests`
  - `streamlit-lottie`
  - `geopandas` (para mapas)
  - `matplotlib` (para algunos gráficos)
  - Cualquier otra que esté en `requirements.txt`

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
   streamlit run app2.py
   ```

2. Abre tu navegador en la dirección que aparece en la terminal (por defecto, [http://localhost:8501](http://localhost:8501)).

3. **Navegación por páginas:**  
   Esta aplicación utiliza un sistema de páginas basado en parámetros de la URL.  
   Para acceder a cada sección principal, debes agregar el parámetro `?page=` en la URL:

   - Para el dashboard principal:
     ```
     http://localhost:8501/?page=dashboard
     ```
   - Para la página de mapas:
     ```
     http://localhost:8501/?page=mapa
     ```

   Si accedes a la aplicación sin el parámetro `?page=`, se mostrará una pantalla de bienvenida.

## Estructura del proyecto

```
streamlit-project/
├── Dashboard.py           # Archivo principal de la aplicación
├── consignaciones.py      # Módulo para la sección de consignaciones
├── incidentes.py          # Módulo para la sección de incidentes
├── resumenApp2.py         # Módulo para la sección de resumen
├── mapa.py                # Módulo para visualización geográfica
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