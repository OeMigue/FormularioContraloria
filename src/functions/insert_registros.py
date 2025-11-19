import xlwings as xw
import gc
import pythoncom

def cerrar_instancia_xlwings(app):
    """
    Cierra únicamente la instancia de Excel creada por xlwings,
    sin cerrar otras instancias abiertas por el usuario,
    limpiando COM y memoria.
    """

    if app is None:
        return

    try:
        # Cierra todos los libros abiertos en esa instancia
        for wb in app.books:
            try:
                wb.close()
            except:
                pass

        # Cierra solo esta instancia
        app.quit()
    except:
        pass

    # Eliminar referencia
    try:
        del app
    except:
        pass

    # Limpiar COM y memoria
    try:
        pythoncom.CoUninitialize()
    except:
        pass

    gc.collect()

    print("Instancia de Excel cerrada correctamente sin afectar otras.")


def insertar_registro_excel(ruta_archivo, hoja_objetivo, columnas, datos, contrasena):
    """Inserta un único registro en Excel"""
    app = xw.App(visible=False)
    app.api.EnableEvents = False
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
    app.api.EnableEvents = True
    wb.save()
    wb.close()
    cerrar_instancia_xlwings(app)

def insertar_multiples_registros(ruta_archivo, hoja_objetivo, columnas, lista_datos, contrasena):
    """Inserta múltiples registros en Excel de una sola vez"""
    app = xw.App(visible=False)
    app.api.EnableEvents = False
    wb = app.books.open(ruta_archivo)
    hoja = wb.sheets[hoja_objetivo]

    hoja.api.Unprotect(Password=contrasena)

    # Encontrar la última fila con datos
    ultima_fila = 1
    for col in columnas:
        col_obj = hoja.range((1, col)).expand('down')
        filas_con_datos = [c.row for c in col_obj if c.value not in [None, ""]]
        if filas_con_datos:
            ultima_fila = max(ultima_fila, max(filas_con_datos))

    # Insertar todos los registros
    for idx, datos in enumerate(lista_datos):
        nueva_fila = ultima_fila + idx + 1
        for i, col in enumerate(columnas):
            hoja.cells(nueva_fila, col).value = datos[i]

    hoja.api.Protect(Password=contrasena)
    app.api.EnableEvents = True
    wb.save()
    wb.close()
    cerrar_instancia_xlwings(app)