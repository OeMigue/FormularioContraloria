import streamlit as st

# Estilo para que el botón parezca solo texto
st.markdown("""
<style>
div.stButton > button {
    background: none;
    border: none;
    color: blue;
    text-decoration: underline;
    cursor: pointer;
    padding: 0;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Botón que luce como texto
if st.button("Texto clicable"):
    st.write("¡Clic detectado!")
