import sys

sys.path.append(
    r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\src\functions"
)

from form_functions import *
from insert_registros import *

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

def limpiar_campos_formulario():
    """Limpia todos los campos del formulario a su estado inicial"""
    st.session_state.año_input = None
    st.session_state.mes_input = None
    st.session_state.concepto_input = None
    st.session_state.especificacion_input = None
    st.session_state.ciudad_input = None
    st.session_state.valor_input = 0

def mostrar_login():
    # Configuración de la página
    st.set_page_config(
        page_title="GCO | Inicio de Sesión",
        page_icon=RUTA_ICON,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    container = st.container()
    with container:
        st.markdown(
            """
                <div class="h2" style='text-align: center; '>
                    <h2>Formulario Informe de Gerencia</h2>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        contenedor_inputs = st.container()
        with contenedor_inputs:
            col01, col02 = st.columns([5, 5])
            with col01:
                col1, col2, col3 = st.columns([12,1,1])
                with col1:
                    st.image(RUTA_BIENVENIDA_GCO, use_container_width=True)
            with col02:
                
                usuario = st.text_input("Usuario:", placeholder="Ej: usuario", icon = ":material/account_circle:")
                contraseña = st.text_input(
                    "Pin:", placeholder="Ej: 1234", type="password", icon = ":material/passkey:")
                enviar = st.button("Iniciar Sesión", icon =":material/login:")
        
            if enviar:
                if not usuario or not contraseña:
                    st.divider()
                    st.warning("Campos obligatorios")
                else:
                    for nombre, datos_bd in CREDENCIALES.items():
                        if usuario == datos_bd[0] and contraseña == datos_bd[1]:
                            st.session_state.autenticado = True
                            st.session_state.usuario_actual = usuario
                            st.session_state.nombre_usuario = nombre
                            @st.dialog('GCO')
                            def ventana_login():
                                st.success(f"Bienvenido(a) {nombre}. Inicio de sesión completo", icon = ":material/how_to_reg:")
                                time.sleep(0.02)
                                st.rerun()
                            ventana_login()
                    st.divider()
                    st.error("Usuario o contraseña incorrectos")        
                        
# Función del formulario
def mostrar_formulario():
    # Limpiar campos si se indica en session_state
    if st.session_state.get("limpiar_campos", False):
        st.session_state.año_input = None
        st.session_state.mes_input = None
        st.session_state.concepto_input = None
        st.session_state.especificacion_input = None
        st.session_state.ciudad_input = None
        st.session_state.valor_input = 0
        st.session_state.limpiar_campos = False

    lista_especificaciones, lista_ciudades, lista_concepto_nuevo, diccionario_unidades = parametros(
        AREAS.get(st.session_state.usuario_actual)
    )
    lista_especificaciones_ordenadas = sorted(lista_especificaciones, key=lambda x: x != "No aplica")
    lista_ciudades_ordenadas = sorted(lista_ciudades, key=lambda x: x != "No aplica")

    # Configuración de la página
    st.set_page_config(
        page_title="GCO | Contraloría",
        page_icon=RUTA_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    containerp = st.container()
    with containerp:
        div1, div2 = st.columns([8, 2])
        with div1:
            # Mostrar usuario actual
            st.success("_" * 10+ f"Bienvenido(a), {st.session_state.nombre_usuario} ✌️"+ "_" * 10, icon = ":material/how_to_reg:")
        with div2:
            cerrar_sesion = st.button("Cerrar Sesión", use_container_width=True)
    st.markdown(
        f"""
            <div class="h2-form" style='text-align: center; border-radius: 30px;'>
                <h2>Formulario {AREAS.get(st.session_state.usuario_actual)}</h2>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption('💡Todos los registros añadidos se puede visualizar al final de la página')
    contenedor_form = st.container()
    with contenedor_form:
        col1, col2 = st.columns(2)
        with col1:
            año_actual = datetime.now().year
            años = [int(año_actual) - 2, int(año_actual) - 1, int(año_actual)]
            año = st.selectbox(
                label="Año:",
                options = años,
                index = None,
                placeholder="Seleccionar una opción...",
                key="año_input"
            )
            concepto = st.selectbox(
                label="Concepto:",
                options=lista_concepto_nuevo,
                index = None,
                placeholder="Seleccionar una opción...",
                key="concepto_input"
            )
            ciudad = st.selectbox(
                label="Ciudad:",
                options=lista_ciudades_ordenadas, 
                index = None,
                placeholder="Seleccionar una opción...",
                key="ciudad_input"
            )
        with col2:
            mes = st.selectbox(
                label="Mes:",
                options= MESES,
                index = None,
                placeholder="Seleccione una opción...",
                key="mes_input"
            )
            especificacion = st.selectbox(
                label="Especificación:",
                options=lista_especificaciones_ordenadas,
                index = None,
                placeholder="Seleccionar una opción...",
                key="especificacion_input"
            )

            # valor = st.number_input(
            #     label=f"Valor:",
            #     format="%f",
            #     step=1.0,
            #     key="valor_input",
            #     icon = ":material/payments:"
            # )

            tipo_valor = diccionario_unidades.get(concepto, "")
            valor = None

            if tipo_valor == "Cantidad":

                valor = st.number_input(
                    label=f"Unidades:",
                    format="%d",
                    step=1,
                    key="valor_input2",
                    icon = ":material/dataset:"
                )

                valor_formateado = locale.format_string("%.0f", valor, grouping=True)
                st.caption(f"Guia: {valor_formateado} Unidades")

            elif tipo_valor == "Pesos":
                valor = st.number_input(
                    label=f"Valor:",
                    format="%d",
                    step=1,
                    key="valor_input2",
                    icon = ":material/payments:"
                )

                valor_formateado = locale.format_string("%.0f", valor, grouping=True)
                st.caption(f"Guia: ${valor_formateado}")

            elif tipo_valor == "Porcentaje":
                valor = st.number_input(
                    label=f"Porcentaje:",
                    format="%f",
                    step=1.0,
                    key="valor_input2",
                    icon = ":material/percent:"
                )

                valor_formateado = locale.format_string("%.0f", valor)
                st.caption(f"Guia: {valor}%")

            elif tipo_valor == "Tonelada":
                valor = st.number_input(
                    label=f"Tonelada:",
                    format="%f",
                    step=1.0,
                    key="valor_input2",
                    icon = ":material/weight:"
                )

                valor_formateado = locale.format_string("%.0f", valor,grouping=True)
                st.caption(f"Guia: {valor_formateado} Tonelada(s)")
            else:
                st.caption("💡Por favor seleccione un concepto")
        
        container_alertas = st.container()
        with container_alertas:
            col_alertas1, col_alertas2, col_alertas3 = st.columns([1, 8, 1])

        st.divider()
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        inputs = {año, mes, concepto, especificacion, ciudad}
        datos = [año, mes, concepto, especificacion, ciudad, valor]
        
        with col_btn1:
            if st.button("Añadir Registro a la Tabla", use_container_width=True, icon = ":material/note_add:"):
                if None in inputs:
                    with col_alertas2:
                        st.warning("Por favor complete todos los campos obligatorios")
                else:
                    st.session_state.registros_tabla.append(datos.copy())
                    with col_alertas2:
                        st.success("✅ Registro añadido a la tabla")
                    # st.session_state.limpiar_campos = True
                    st.rerun()
        
        with col_btn2:
            if st.button("Limpiar Tabla", use_container_width=True, icon=":material/mop:"):
                if st.session_state.registros_tabla:

                    @st.dialog('¿Está seguro(a) de limpiar la tabla?')
                    def ventana_limpiar_papelera():
                        if st.button('Limpiar Tabla'):
                            st.session_state.registros_tabla = []
                            st.session_state.limpiar_campos = True
                            st.rerun()
                    ventana_limpiar_papelera()
                else:
                    with col_alertas2:
                        st.warning("Todavía no hay registros")
        
        with col_btn3:
            registros_pendientes = len(st.session_state.registros_tabla)
            if st.button(f"Enviar Todo ({registros_pendientes})", use_container_width=True, icon = ":material/drive_file_move:"):
                        if registros_pendientes == 0:
                            with col_alertas2:
                                st.warning("No hay registros para enviar")
                        else:
                            @st.dialog('¿Seguro(a) de enviar los registros?')
                            def ventana_enviar_todo():
                                if st.button('Enviar Registros'):
                                    with st.spinner("Enviando registros..."):
                                        hilo_guardar = threading.Thread(
                                            target=ejecutar_guardar_multiples,
                                            args=(st.session_state.registros_tabla, st.session_state.usuario_actual),
                                            )
                                        hilo_guardar.start()
                                        barra_carga = st.progress(0)
                                        progreso = 0
                                        while hilo_guardar.is_alive():
                                            progreso = (progreso + 10) % 100
                                            barra_carga.progress(progreso)
                                            time.sleep(0.3)
                                        barra_carga.empty()
                                        st.toast("Registros enviados con éxito", icon="✅")
                                        with col_alertas2:
                                            st.success(f"✅ Se enviaron {registros_pendientes} registro(s)")
                                        st.session_state.registros_tabla = []
                                        st.session_state.limpiar_campos = True
                                        time.sleep(1)
                                        st.rerun()
                            ventana_enviar_todo()

        # Mostrar tabla de registros
        if st.session_state.registros_tabla:
            # st.divider()
            st.subheader("📋 Registros en la tabla:")
            

            # Crear DataFrame de los registros
            columnas = ["Año", "Mes", "Concepto", "Especificación", "Ciudad", "Valor"]
            df_registros = pd.DataFrame(st.session_state.registros_tabla, columns=columnas)
            
            # Mostrar tabla con opción de eliminar
            col_tabla1, col_tabla2 = st.columns([9, 1])
            
            with col_tabla1:
                st.dataframe(df_registros, height=len(st.session_state.registros_tabla) * 35 + 37, hide_index=True)

            def eliminar_registro():
                # Revisar todos los checkboxes y eliminar los que están seleccionados
                for idx in range(len(st.session_state.registros_tabla) - 1, -1, -1):
                    checkbox_key = f"checkbox_{idx}"
                    if checkbox_key in st.session_state and st.session_state[checkbox_key]:
                        st.session_state.registros_tabla.pop(idx)
                        st.session_state[checkbox_key] = False

            with col_tabla2:
                container_eliminar = st.container()
                with container_eliminar:
                    st.caption('Eliminar fila')
                    for idx in range(len(st.session_state.registros_tabla)):
                        st.checkbox(f"❌", key=f"checkbox_{idx}", on_change=eliminar_registro)

        if cerrar_sesion:
            @st.dialog('¿Está seguro(a) de cerrar sesión?')
            def ventana_cerrar_sesion():
                if st.button('Confirmar Cerrar Sesión', icon=":material/logout:"):
                    st.session_state.autenticado = False
                    st.session_state.usuario_actual = ""
                    st.session_state.registros_tabla = []
                    st.rerun()
            ventana_cerrar_sesion()

# ===========================================================================================================================================

# Main
def main():
    aplicar_css()

    # Inicializar session_state
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if "usuario_actual" not in st.session_state:
        st.session_state.usuario_actual = ""
    if "registros_tabla" not in st.session_state:
        st.session_state.registros_tabla = []
    if "limpiar_campos" not in st.session_state:
        st.session_state.limpiar_campos = False

    st.sidebar.image(RUTA_IMAGE)

    if st.session_state.autenticado:
        mostrar_formulario()
    else:
        mostrar_login()
    st.divider()
    st.image(RUTA_ICON_MARCAS, use_container_width=True)

if __name__ == "__main__":
    main()