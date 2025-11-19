import streamlit as st
import pandas as pd
import openpyxl as opxl
import time
from datetime import datetime
import locale
import threading

locale.setlocale(locale.LC_ALL, '')  # Usa configuración local del sistema

RUTA_CSS = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\styles\COLORES.css"
RUTA_IMAGE = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\images\GContraloria.png"
RUTA_ICON = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\images\gco_ico.svg"
RUTA_ARCHIVO = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\input\Ingreso Datos Informe Gerencia Contraloria - Eficiencias y Volumetria.xlsm"
RUTA_ICON_CERRAR_SESION = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\images\CerrarSesion.png"
RUTA_ICON_MARCAS = r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\images\footer_marcas.svg"

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
    "jorgeeh": "Analítica de Contraloría",
    "albertoc": "Control de Operaciones",
    "oscardy": "Administrativa",
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

    if area == "Analítica de Contraloría" or area == "Admin":
        lista_concepto_nuevo = df.iloc[:,22].dropna().drop_duplicates().tolist()
    elif area == "Control de Operaciones":
        lista_concepto_nuevo = df.iloc[:,38].dropna().drop_duplicates().tolist()
    elif area == "Administrativa":
        lista_concepto_nuevo = df.iloc[:,10].dropna().drop_duplicates().tolist()
    elif area == "Riesgos y Cumplimiento":
        lista_concepto_nuevo = df.iloc[:,50].dropna().drop_duplicates().tolist()
    elif area == "Impuestos":
        lista_concepto_nuevo = df.iloc[:,46].dropna().drop_duplicates().tolist()
    elif area == "Contabilidad":
        lista_concepto_nuevo = df.iloc[:,30].dropna().drop_duplicates().tolist()

    return lista_especificaciones, lista_ciudades, lista_concepto_nuevo

def ejecutar_guardar(año, mes, concepto, especificacion, ciudad, valor, usuario_actual):
    """Guarda un único registro en Excel (función legacy)"""
    from insert_registros import insertar_registro_excel

    # Elegimos la hoja según el usuario
    if usuario_actual == "jorgeeh":
        hoja = "Analítica de Contraloría"
    elif usuario_actual == "albertoc":
        hoja = "Control de Operaciones"
    elif usuario_actual == "oscardy":
        hoja = "Administrativa"
    elif usuario_actual == "doragc":
        hoja = "Riesgos y Cumplimiento"
    elif usuario_actual == "zrestrepo":
        hoja = "Impuestos"
    elif usuario_actual == "anamr":
        hoja = "Contabilidad"
    else:
        hoja = "Admin"

    # Guardamos los datos en el archivo Excel
    insertar_registro_excel(
        ruta_archivo=RUTA_ARCHIVO,
        hoja_objetivo=hoja,
        columnas=[1, 2, 4, 7, 8, 11],
        datos=[año, mes, concepto, especificacion, ciudad, valor],
        contrasena="54312"
    )

def ejecutar_guardar_multiples(registros, usuario_actual):
    """Guarda múltiples registros en Excel de una sola vez"""
    from insert_registros import insertar_multiples_registros

    # Elegimos la hoja según el usuario
    if usuario_actual == "jorgeeh":
        hoja = "Analítica de Contraloría"
    elif usuario_actual == "albertoc":
        hoja = "Control de Operaciones"
    elif usuario_actual == "oscardy":
        hoja = "Administrativa"
    elif usuario_actual == "doragc":
        hoja = "Riesgos y Cumplimiento"
    elif usuario_actual == "zrestrepo":
        hoja = "Impuestos"
    elif usuario_actual == "anamr":
        hoja = "Contabilidad"
    else:
        hoja = "Admin"

    # Guardamos todos los datos en el archivo Excel
    insertar_multiples_registros(
        ruta_archivo=RUTA_ARCHIVO,
        hoja_objetivo=hoja,
        columnas=[1, 2, 4, 7, 8, 11],
        lista_datos=registros,
        contrasena="54312"
    )

if __name__ == "__main__":
    # parametros()
    print("No es")