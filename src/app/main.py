import sys
sys.path.append(r"O:\Gerencia Contraloria\Analitica Contraloria\Automatiaciones Ambiente Pruebas\Carpeta Miguel Cardona\FORMULARIOS\src\functions")

from form_functions import *
from insert_registros import *



# Inicializar session_state
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario_actual" not in st.session_state:
    st.session_state.usuario_actual = ""

def mostrar_login():
    # Configuración de la página
    st.set_page_config(
        page_title="GCO | Inicio de Sesión",
        page_icon= RUTA_ICON,
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
                    st.warning("Campos obligatorios")
                else:
                    for nombre, datos_bd in CREDENCIALES.items():
                        if usuario == datos_bd[0] and contraseña == datos_bd[1]:
                            st.session_state.autenticado = True
                            st.session_state.usuario_actual = usuario
                            st.session_state.nombre_usuario = nombre
                            st.success(
                                f"Bienvenido {nombre}. Inicio de sesión completo"
                            )
                            time.sleep(1)
                            st.rerun()
                    st.error("Usuario o contraseña incorrectos")

# Función del formulario
def mostrar_formulario():
    lista_especificaciones, lista_ciudades, lista_concepto_anterior = parametros(AREAS.get(st.session_state.usuario_actual))

    # Configuración de la página
    st.set_page_config(
        page_title="GCO | Formulario",
        page_icon=RUTA_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    containerp = st.container()
    with containerp:
        div1, div2 = st.columns([8, 2])
        with div1:
            # Mostrar usuario actual
            st.success("_"*10 + f"Bienvenido/a, {st.session_state.nombre_usuario} ✌️" + "_"*10)
        
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

    contenedor_form = st.container()
    with contenedor_form:
        col1, col2 = st.columns(2)

        with col1:
            año_actual = datetime.now().year
            años = [int(año_actual) - 1, int(año_actual), int(año_actual) + 1]

            año = st.selectbox(label="Año:", options=["Seleccione una Opción..."]+años,placeholder="Seleccionar una opción...")            
            concepto = st.selectbox(label="Concepto Anterior:", options=["Seleccione una Opción..."]+lista_concepto_anterior, placeholder="Seleccionar una opción...")
            ciudad = st.selectbox(label="Ciudad:", options=["Seleccione una Opción..."]+lista_ciudades, placeholder="Seleccionar una opción...")

        with col2:
            mes = st.selectbox(label="Mes:", options=["Seleccione una Opción..."]+MESES, placeholder="Seleccione una opción...")
            especificacion = st.selectbox(label="Especificación:", options=["Seleccione una Opción..."]+lista_especificaciones, placeholder="Seleccionar una opción...")
            valor = st.number_input(label='Valor:', placeholder="Escribe un valor válido...")

        st.divider()
        enviar_form = st.button("Enviar Formulario", use_container_width=True)



        if enviar_form:
            inputs = {año, mes, concepto, especificacion, ciudad}
            if "Seleccione una Opción..." in inputs:
                st.warning("Por favor complete todos los campos obligatorios")
            else:
                datos=[año, mes, concepto, especificacion]
                # df = pd.DataFrame(datos, columns=['Año', 'Mes', 'Concepto', 'Especificación', 'ciudad', 'valor'])
                # st.dataframe(df)
                with st.spinner("Enviando formulario..."):
                    progress_bar = st.progress(1)
                    for porcentaje in range(100):
                        time.sleep(0.05)  # Simula el proceso
                        progress_bar.progress(porcentaje + 1)

                st.toast("Formulario enviado con éxito", icon="✅")
                insertar_registro_excel(ruta_archivo=RUTA_ARCHIVO, hoja_objetivo="Analítica de Contraloría", columnas=[1, 2, 4, 7, 8, 11],datos=[año, mes, concepto, especificacion, ciudad, f"{valor:.0f}"], contrasena="54312")

        if cerrar_sesion:
            st.session_state.autenticado = False
            st.session_state.usuario_actual = ""
            st.rerun()
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
