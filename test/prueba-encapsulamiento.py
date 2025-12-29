import streamlit as st

RUTA_CSS = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\test\encapsulamiento.css"

def aplicar_css():
    with open(RUTA_CSS, mode="r", encoding="utf-8") as f:
        css = f.read()
    st.markdown(
        f""" 
    <style>
        {css}
    </style> 
    """,
        unsafe_allow_html=True,
    )
    
aplicar_css()

st.markdown('<div class="login-form">', unsafe_allow_html=True)

st.text_input("Usuario")
st.text_input("Pin", type="password")

st.markdown('<div class="btn-submit">', unsafe_allow_html=True)
st.button("Ingresar")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)