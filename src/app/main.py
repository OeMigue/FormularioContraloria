import sys

sys.path.append(
    r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\src\functions"
)

from form_functions import *
from insert_registros import *

# Inicializar session_state
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""
if "registros_tabla" not in st.session_state:
    st.session_state.registros_tabla = []

def mostrar_login():
    # Configuración de la página
    st.set_page_config(
        page_title="GCO | Inicio de Sesión",
        page_icon=RUTA_ICON,
        layout="centered",
        initial_sidebar_state="expanded",
    )
    div002 = st.container()
    with div002:
        pass
    container = st.container()
    with container:
        st.markdown(
            """
                <div class="h2" style='text-align: center; border-radius: 30px;'>
                    <h2>Iniciar Sesión</h2>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()
        contenedor_inputs = st.container()
        with contenedor_inputs:
            col01, col02, col03 = st.columns([1, 5, 1])
            with col02:
                usuario = st.text_input("Usuario:", placeholder="Ej: usuario")
                contraseña = st.text_input(
                    "Pin:", placeholder="Ej: 1234", type="password"
                )
                enviar = st.button("Iniciar Sesión")
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
                                    st.success(
                                        f"Bienvenido {nombre}. Inicio de sesión completo"
                                    )
                                    time.sleep(0.02)
                                    st.rerun()
                                ventana_login()
                        st.divider()
                        st.error("Usuario o contraseña incorrectos")

# Función del formulario
def mostrar_formulario():
    lista_especificaciones, lista_ciudades, lista_concepto_nuevo = parametros(
        AREAS.get(st.session_state.usuario_actual)
    )
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
            st.success(
                "_" * 10
                + f"Bienvenido/a, {st.session_state.nombre_usuario} ✌️"
                + "_" * 10
            )
        with div2:
            cerrar_sesion = st.button("Cerrar Sesión", width='stretch')
    st.markdown(
        f"""
            <div class="h2-form" style='text-align: center; border-radius: 30px;'>
                <h2>Formulario {AREAS.get(st.session_state.usuario_actual)}</h2>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption('💡Todos los registros añadidos se puede visualizar al final de la pagina')
    contenedor_form = st.container()
    with contenedor_form:
        col1, col2 = st.columns(2)
        with col1:
            año_actual = datetime.now().year
            años = [int(año_actual) - 1, int(año_actual), int(año_actual) + 1]
            año = st.selectbox(
                label="Año:",
                options=["Seleccione una Opción..."] + años,
                placeholder="Seleccionar una opción...",
                key="año_input"
            )
            concepto = st.selectbox(
                label="Concepto Anterior:",
                options=["Seleccione una Opción..."] + lista_concepto_nuevo,
                placeholder="Seleccionar una opción...",
                key="concepto_input"
            )
            ciudad = st.selectbox(
                label="Ciudad:",
                options=["Seleccione una Opción..."] + lista_ciudades,
                placeholder="Seleccionar una opción...",
                key="ciudad_input"
            )
        with col2:
            mes = st.selectbox(
                label="Mes:",
                options=["Seleccione una Opción..."] + MESES,
                placeholder="Seleccione una opción...",
                key="mes_input"
            )
            especificacion = st.selectbox(
                label="Especificación:",
                options=["Seleccione una Opción..."] + lista_especificaciones,
                placeholder="Seleccionar una opción...",
                key="especificacion_input"
            )
            valor = st.number_input(
                label=f"Valor:",
                placeholder="Escribe un valor válido...",
                format="%.0f",
                step=1000.00,
                key="valor_input"
            )
            valor_formateado = locale.format_string("%.0f", valor, grouping=True)
            col01, col02 = st.columns([1, 1])
            with col01:
                st.caption(f"Guia del valor: ${valor_formateado}")
        
        container_alertas = st.container()
        with container_alertas:
            col_alertas1, col_alertas2, col_alertas3 = st.columns([1, 8, 1])

        st.divider()
        
        # Botones de acción
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        
        inputs = {año, mes, concepto, especificacion, ciudad}
        datos = [año, mes, concepto, especificacion, ciudad, valor]
        
        with col_btn1:
            if st.button("➕ Añadir Registro a la Tabla", width='stretch'):
                if "Seleccione una Opción..." in inputs:
                    with col_alertas2:
                        st.warning("Por favor complete todos los campos obligatorios")
                else:
                    st.session_state.registros_tabla.append(datos.copy())
                    with col_alertas2:
                        st.success("✅ Registro añadido a la tabla")
                    st.rerun()
        
        with col_btn2:
            if st.button("🗑️ Limpiar Tabla", width='stretch'):
                @st.dialog('¿Seguro(a)?')
                def ventana_limpiar_papelera():
                    if st.button('Limpiar Tabla'):
                        st.session_state.registros_tabla = []
                        st.rerun()
                ventana_limpiar_papelera()
        
        with col_btn3:
            registros_pendientes = len(st.session_state.registros_tabla)
            if st.button(f"📤 Enviar Todo ({registros_pendientes})", width='stretch'):
                @st.dialog('¿Seguro(a) de enviar los registros?')
                def ventana_enviar_todo():
                    if st.button('Enviar Registros'):
                        if registros_pendientes == 0:
                            with col_alertas2:
                                st.warning("No hay registros para enviar")
                        else:
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
                                time.sleep(1)
                                st.rerun()
                ventana_enviar_todo()

        # Mostrar tabla de registros
        if st.session_state.registros_tabla:
            st.divider()
            st.subheader("📋 Registros en la tabla:")
            

            # Crear DataFrame de los registros
            columnas = ["Año", "Mes", "Concepto", "Especificación", "Ciudad", "Valor"]
            df_registros = pd.DataFrame(st.session_state.registros_tabla, columns=columnas)
            
            # Mostrar tabla con opción de eliminar
            col_tabla1, col_tabla2 = st.columns([8, 2])
            
            with col_tabla1:
                st.dataframe(df_registros, width='stretch', hide_index=True)
            
            with col_tabla2:
                st.caption('...................................................')
                for idx in range(len(st.session_state.registros_tabla)):
                    if st.button(f"❌ Fila {idx + 1}", width='stretch', key=f"delete_{idx}"):
                        st.session_state.registros_tabla.pop(idx)
                        st.rerun()

        if cerrar_sesion:
            @st.dialog('¿Seguro(a)?')
            def ventana_cerrar_sesion():
                if st.button('Cerrar Sesión', icon=":material/logout:"):
                    st.session_state.autenticado = False
                    st.session_state.usuario_actual = ""
                    st.session_state.registros_tabla = []
                    st.rerun()
            ventana_cerrar_sesion()

# ===========================================================================================================================================

# Main
def main():
    aplicar_css()
    st.sidebar.image(RUTA_IMAGE)

    if st.session_state.autenticado:
        mostrar_formulario()
    else:
        mostrar_login()
        
if __name__ == "__main__":
    main()