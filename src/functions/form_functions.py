import streamlit as st
import pandas as pd
import openpyxl as opxl
import time
from datetime import datetime

RUTA_CSS = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\styles\COLORES.css"
RUTA_IMAGE = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\Streamlit\images\GContraloria.jpeg"
RUTA_ICON = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\images\gco_ico.svg"
RUTA_ARCHIVO = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\input\Ingreso Datos Informe Gerencia Contraloria - Eficiencias y Volumetria.xlsm"

CREDENCIALES = {
    "Miguel Cardona": ["mcardona", "777"],
    "Jorge Herrera": ["jorgeeh", "1212"],
    "Alberto Cortes": ["albertoc", "2323"],
    "Oscar Yepes": ["oscardy", "3434"],
    "Dora Gomez": ["doragc", "4545"],
    "Zaneida Restrepo": ["zrestrepo", "5656"],
    "Ana Romero": ["anamr", "6767"],
}

AREAS = {
    "mcardona": "Admin",
    "jorgeeh": "Analítica Contraloría",
    "albertoc": "Control de Operaciones",
    "oscardy": "Administrativo",
    "doragc": "Riesgos y Cumplimiento",
    "zrestrepo": "Impuestos",
    "anamr": "Contabilidad",
}

MESES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


# Función para el CSS
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

def parametros(area):
    
    df = pd.read_excel(
        io=RUTA_ARCHIVO,
        sheet_name="Parámetros",
        skiprows=1,
    )

    lista_especificaciones = df.iloc[:,14].dropna().drop_duplicates().tolist()
    lista_ciudades = df.iloc[:,16].dropna().drop_duplicates().tolist()

    if area == "Analítica Contraloría" or area == "Admin":
        lista_concepto_anterior = df.iloc[:,22].dropna().drop_duplicates().tolist()
    elif area == "Control de Operaciones":
        lista_concepto_anterior = df.iloc[:,38].dropna().drop_duplicates().tolist()
    elif area == "Administrativo":
        lista_concepto_anterior = df.iloc[:,10].dropna().drop_duplicates().tolist()
    elif area == "Riesgos y Cumplimiento":
        lista_concepto_anterior = df.iloc[:,50].dropna().drop_duplicates().tolist()
    elif area == "Impuestos":
        lista_concepto_anterior = df.iloc[:,46].dropna().drop_duplicates().tolist()
    elif area == "Contabilidad":
        lista_concepto_anterior = df.iloc[:,30].dropna().drop_duplicates().tolist()

    return lista_especificaciones,lista_ciudades,lista_concepto_anterior

if __name__ == "__main__":
    parametros()
    # print("No es")