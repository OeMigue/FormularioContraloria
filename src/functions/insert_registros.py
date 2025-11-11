import xlwings as xw

def insertar_registro_excel(ruta_archivo, hoja_objetivo, columnas, datos, contrasena):
    app = xw.App(visible=False)
    wb = app.books.open(ruta_archivo)
    hoja = wb.sheets[hoja_objetivo]

    hoja.api.Unprotect(Password=contrasena)

    ultima_fila = 1
    for col in columnas:
        col_obj = hoja.range((1, col)).expand('down')
        filas_con_datos = [c.row for c in col_obj if c.value not in [None, ""]]
        if filas_con_datos:
            ultima_fila = max(ultima_fila, max(filas_con_datos))

    nueva_fila = ultima_fila + 1

    for i, col in enumerate(columnas):
        hoja.cells(nueva_fila, col).value = datos[i]

    hoja.api.Protect(Password=contrasena)
    wb.save()
    wb.close()
    app.quit()

# Ejemplo de uso:
insertar_registro_excel(
    ruta_archivo=r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\input\Ingreso Datos Informe Gerencia Contraloria - Eficiencias y Volumetria.xlsm",
    hoja_objetivo="Analítica de Contraloría",
    columnas=[1, 2, 4, 7, 8, 11],
    datos=[2050, 'febrero', "Puntos a conciliar", 'No aplica', "No aplica", '5000000'],
    contrasena="54312"
)