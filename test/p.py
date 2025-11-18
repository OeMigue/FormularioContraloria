import streamlit as st
import time as t

if st.button('Enviar'):
    @st.dialog('Ventana')
    def ventana():
        t.sleep(2)
        st.rerun()
    ventana()