import streamlit as st

v = st.text_input(label='palabra')
validacion=['.',',',';',':','-','_',]
for n in validacion:
    while v != n:
        pass
