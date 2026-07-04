"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import glob
    import pandas as pd
    import os

    directorio = "files/input"

    files = glob.glob(f"{directorio}/bank-marketing-campaing-*.csv.zip")

    almacenar_dfs  =  []

    for file in files:

        temp = pd.read_csv(file, compression="zip")

        almacenar_dfs.append(temp)  
    df = pd.concat(almacenar_dfs, ignore_index=True)

    map_meses = {"jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", "jun": "06",
                 "jul": "07", "aug": "08", "sep": "09", "oct": "10", "nov": "11", "dec": "12"
                 }

    columnas_clientes = ["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]

    client_df = df[columnas_clientes].copy()

    client_df["job"] = client_df["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client_df["education"] = client_df["education"].str.replace(".", "_", regex=False).replace("unknown", pd.NA)
    client_df["credit_default"] = client_df["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].apply(lambda x: 1 if x == "yes" else 0)    

    days = df["day"].astype(str).str.zfill(2)
    months = df["month"].str.lower().map(map_meses)
    df["last_contact_day"] = "2022-" + months + "-" + days

    campaign_columnas = [
        "client_id", "number_contacts", "contact_duration", 
        "previous_campaign_contacts", "previous_outcome", 
        "campaign_outcome", "last_contact_day"
    ]
    campaign_df = df[campaign_columnas].copy()

    campaign_df = campaign_df.rename(columns={"last_contact_day": "last_contact_date"})
    
    # Aplicar transformaciones solicitadas
    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)

    if "eurobor_three_months" not in df.columns and "euribor_three_months" in df.columns:
        df = df.rename(columns={"euribor_three_months": "eurobor_three_months"})
        
    economics_cols = ["client_id", "cons_price_idx", "eurobor_three_months"]
    
    economics_df = df[economics_cols].copy()
    # Renombrar para cumplir estrictamente la salida requerida
    economics_df.columns = ["client_id", "cons_price_idx", "euribor_three_months"]

    output_directory = "files/output"
    os.makedirs(output_directory, exist_ok=True)
    
    client_df.to_csv(f"{output_directory}/client.csv", index=False)
    campaign_df.to_csv(f"{output_directory}/campaign.csv", index=False)
    economics_df.to_csv(f"{output_directory}/economics.csv", index=False)



if __name__ == "__main__":
    clean_campaign_data()
