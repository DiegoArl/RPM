import pandas as pd
import re

def leer_archivo(archivo):
    nombre = archivo.name.lower()

    if nombre.endswith(".csv"):
        return pd.read_csv(archivo, low_memory=False)
    elif nombre.endswith((".xlsx", ".xls")):
        return pd.read_excel(archivo)
    
    else:
        raise ValueError("Formato no soportado")
    

def leer_archivo_encuesta(archivo):

    hojas = {
        'Ventas': 'df_Ventas',
        'Cuotas': 'df_Cuotas',
        'Encuesta': 'df_Encuesta',
        'Relación': 'df_Relacion',
        'CambioRUC': 'df_CambioRUC'
    }

    def combinar_normalizar(a, b):
        meses = {
            "ene":"01","feb":"02","mar":"03","abr":"04","may":"05","jun":"06",
            "jul":"07","ago":"08","set":"09","sep":"09","oct":"10",
            "nov":"11","dic":"12"
        }

        if pd.isna(a) and pd.isna(b):
            return None
        if pd.isna(a):
            return str(b)
        if pd.isna(b):
            return str(a)

        a_str = str(a).strip()
        b_str = str(b).strip()

        if b_str in meses and re.fullmatch(r"\d{4}", a_str):
            return f"{a_str}-{meses[b_str]}"

        return f"{a_str}-{b_str}"

    archivo.seek(0)
    xls = pd.read_excel(archivo, sheet_name=None, header=None)

    resultados = {}

    for hoja, nombre_variable in hojas.items():
        df_raw = xls[hoja]

        if hoja == 'Ventas':
            h1 = df_raw.iloc[0]
            h2 = df_raw.iloc[1]

            headers_final = [combinar_normalizar(a, b) for a, b in zip(h1, h2)]

            df_data = df_raw.iloc[2:].reset_index(drop=True)
            df_data.columns = headers_final
        else:
            df_data = df_raw.iloc[1:].reset_index(drop=True)
            df_data.columns = df_raw.iloc[0]

        if "Total general" in df_data.columns:
            df_data = df_data.drop(columns=["Total general"])

        primera_col = df_data.columns[0]

        df_data = df_data[
            df_data[primera_col].astype(str).str.lower() != "total general"
        ]

        resultados[nombre_variable] = df_data
        
    return resultados