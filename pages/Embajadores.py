import streamlit as st
from Scripts.salidas import df_a_excel
from Scripts.carga import leer_archivo_encuesta
from Scripts.encuesta import procesar_flujo_embajadores

st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:first-child {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.header("Encuesta Embajadores")

archivo_embajadores = st.file_uploader(
    "Sube el excel con el archivo de embajadores (Ventas, Cuotas, Encuesta, Relacion, CambioRUC)",
    type=["xlsx"]
)

@st.cache_data
def procesar_embajadores_cached(df):
    return procesar_flujo_embajadores(df)

@st.cache_data
def generar_excel_cached(df):
    return df_a_excel(df)

if archivo_embajadores:
    try:
        st.session_state.embajadores = leer_archivo_encuesta(archivo_embajadores)
        st.success("Archivo subido correctamente")

    except Exception as e:
        st.error(str(e))

if "embajadores" not in st.session_state:
    st.warning("No se ha cargado el archivo de embajadores")
    st.stop()

df = st.session_state["embajadores"]

try:

    df_final = procesar_embajadores_cached(df)

    if df_final is None or df_final.empty:
        st.error("El procesamiento no generó resultados")
        st.stop()

    excel_file = generar_excel_cached(df_final)

except Exception:
    st.error("Error procesando el archivo. Verifique el formato o cambie de archivo.")
    del st.session_state["embajadores"]
    st.stop()

st.subheader("Archivo Embajadores")
st.write(f"Filas: {df_final.shape[0]} | Columnas: {df_final.shape[1]}")
st.dataframe(df_final.head())

nombre_archivo = "Embajadores_Procesado.xlsx"

st.download_button(
    label="Descargar Excel",
    data=excel_file,
    file_name=nombre_archivo,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)