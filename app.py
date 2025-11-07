import streamlit as st

# -------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APP
# -------------------------------------------------
st.set_page_config(
    page_title="BiotechSuperfood IA",
    page_icon="🌿",
    layout="centered",
)

# -------------------------------------------------
# CSS PERSONALIZADO (colores, botones, fondo)
# -------------------------------------------------
st.markdown("""
    <style>
    /* Fondo general con degradado */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #E9F5FF 0%, #FFFFFF 100%);
    }
    /* Título principal */
    h1, h2, h3 {
        color: #0056B3 !important;
        font-weight: 700 !important;
    }
    /* Botones */
    div.stButton > button {
        background-color: #0078D7;
        color: white;
        border-radius: 10px;
        height: 45px;
        font-weight: bold;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #0056B3;
        color: #E0EFFF;
    }
    /* Cuadro de entrada */
    .stTextInput input {
        border: 1px solid #0078D7;
        border-radius: 8px;
    }
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #0078D7;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# IMÁGENES BASE (usa enlaces online)
# -------------------------------------------------
IMAGEN_LOGO = "https://cdn-icons-png.flaticon.com/512/4149/4149723.png"
IMAGEN_IA = "https://cdn-icons-png.flaticon.com/512/4712/4712105.png"
IMAGEN_FORMULA = "https://cdn-icons-png.flaticon.com/512/1048/1048947.png"

# -------------------------------------------------
# INICIALIZAR VARIABLES DE SESIÓN
# -------------------------------------------------
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "usuario" not in st.session_state:
    st.session_state.usuario = None
if "pais" not in st.session_state:
    st.session_state.pais = ""
if "categoria" not in st.session_state:
    st.session_state.categoria = ""
if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []
if "organolepticos" not in st.session_state:
    st.session_state.organolepticos = []


def reset_pasos():
    st.session_state.paso = 1
    st.session_state.pais = ""
    st.session_state.categoria = ""
    st.session_state.ingredientes = []
    st.session_state.organolepticos = []
    st.session_state.usuario = None

# -------------------------------------------------
# LOGIN
# -------------------------------------------------
if st.session_state.usuario is None:
    st.image(IMAGEN_LOGO, width=120)
    st.title("🌿 ¡Bienvenido a BiotechSuperfood IA!")
    st.subheader("Optimiza tus fórmulas con Inteligencia Artificial 💡")
    st.write("Ingrese sus credenciales para continuar:")

    usuario = st.text_input("👤 Usuario")
    contraseña = st.text_input("🔒 Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "admin" and contraseña == "1234":
            st.session_state.usuario = usuario
            st.success("Inicio de sesión exitoso ✅")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

# -------------------------------------------------
# PASO 1: PAÍS
# -------------------------------------------------
elif st.session_state.paso == 1:
    st.image(IMAGEN_LOGO, width=80)
    st.header("🌎 Paso 1: Selección de país")
    st.session_state.pais = st.selectbox("Seleccione un país", ["", "Perú", "Colombia", "México"])

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", disabled=True)
    with col2:
        if st.button("Siguiente") and st.session_state.pais:
            st.session_state.paso = 2
            st.rerun()

# -------------------------------------------------
# PASO 2: CATEGORÍA
# -------------------------------------------------
elif st.session_state.paso ==_


