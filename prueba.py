import requests
import json
import pandas as pd
import matplotlib.pyplot as plt

dataset_id = 'EC6945'
start_date = '2025-05-03'
end_date = '2025-05-03'
columnDestinyName = 'null' # Ingrese el nombre de la columna destino a filtrar. De lo contrario null
values= 'null' # Ingrese el valor(es) por lo que desea filtrar. Obligatorio si ingresa columnDestinyName. Ejm:1,3,2 De lo contrario null

url = f"https://www.simem.co/backend-files/api/PublicData?startDate={start_date}&enddate={end_date}&datasetId={dataset_id}&columnDestinyName={columnDestinyName}&values={values}"
response = requests.get(url)


# Organizar la respuesta en un formato legible
if response.status_code == 200:
    data = json.loads(response.content)
    print(json.dumps(data, indent=4))  # Imprimir la respuesta con formato JSON legible
    records = data.get("result", {}).get("records", [])
    if not records:
        print("No se encontraron datos en la respuesta de la API.")
    else:
        # Convertir los registros a un DataFrame
        df = pd.DataFrame(records)

        # Mostrar el DataFrame
        print("Datos extraídos:")
        print(df)

    df['FechaHora'] = pd.to_datetime(df['FechaHora'])

    # Graficar
    plt.figure(figsize=(10, 6))
    for variable in df['CodigoVariable'].unique():
        subset = df[df['CodigoVariable'] == variable]
        plt.plot(subset['FechaHora'], subset['Valor'], label=variable)

    plt.title('Valores por FechaHora')
    plt.xlabel('FechaHora')
    plt.ylabel('Valor (COP/kWh)')
    plt.legend()
    plt.grid()
    plt.show()
else:
    print(f"Error en la solicitud: {response.status_code}")