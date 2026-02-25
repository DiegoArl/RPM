import streamlit as st

st.set_page_config(
    page_title= "Reportes",
    layout="wide"
)

st.title("Página principal")

st.markdown("""
<style>
[data-testid="stSidebarNav"] ul li:first-child {
    display: none;
}
</style>
""", unsafe_allow_html=True)

st.page_link("pages/Embajadores.py", label="Ir a Embajadores")
