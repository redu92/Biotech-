import streamlit as st
from openai import OpenAI
import os

# Configuración de la página
st.set_page_config(
    page_title="BiotechSuperfood IA",
    page_icon="biotech.jpg",
    layout="centered"
)

# ========= ESTILOS CSS ==========
st.markdown("""
    <style>
        /* Fondo general */
        body {
            background-color: #f5f8fa;
            color: #222;
        }

        /* Header azul */
        .main-header {
            display: flex;
            align-items: center;
            background-color: #0077b6;
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .main-header img {
            height: 60px;
            margin-right: 15px;
            border-radius: 8px;
        }

        .main-header h1 {
            font-size: 1.8rem;
            margin: 0;
        }

        .stButton>button {
            background-color: #0077b6;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
        }

        .stButton>button:hover {
            background-color: #023e8a;
        }

        .login-box {
            background-color: white;
            padding: 2rem;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

# ========= ENCABEZADO ==========
st.markdown(
    """
    <div class="main-header">
        <img src="biotech.jpg" alt="Biotech Logo">
        <h1>BiotechSuperfood · Panel IA</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ========= CONFIGURACIÓN ==========
# Inicializa variables de sesión
if "paso" not in st.session_state:
    st.session_state.paso = 1
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []

# ========= PASO 1: LOGIN ==========
if st.session_state.paso == 1:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.subheader("🔐 Inicia sesión")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "admin" and password == "biotech2025":
            st.session_state.usuario = usuario
            st.session_state.paso = 2
            st.success("Inicio de sesión exitoso ✅")
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.markdown("</div>", unsafe_allow_html=True)

# ========= PASO 2: SELECCIÓN ==========
elif st.session_state.paso == 2:
    st.subheader("🥑 Selecciona tus parámetros nutricionales")

    opciones = [
        "Proteína alta",
        "Bajo en sodio",
        "Rico en antioxidantes",
        "Apto para veganos",
        "Alto en fibra",
        "Energético"
    ]

    seleccionados = []
    for i, k in enumerate(opciones):
        checked = st.checkbox(k, key=f"check_{i}", value=(k in st.session_state.ingredientes))
        if checked:
            seleccionados.append(k)

    if st.button("Generar recomendación"):
        st.session_state.ingredientes = seleccionados
        st.session_state.paso = 3
        st.rerun()

# ========= PASO 3: RESULTADO CON OPENAI ==========
elif st.session_state.paso == 3:
    st.subheader("🤖 Resultados personalizados")

    # Inicializa cliente OpenAI (requiere tu API Key)
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if st.session_state.ingredientes:
        prompt = f"""
        Eres un experto en nutrición funcional. Con base en los siguientes parámetros:
        {', '.join(st.session_state.ingredientes)},
        recomienda tres productos superfood de la marca Biotech y explica brevemente por qué.
        """

        try:
            respuesta = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en nutrición y superfoods."},
                    {"role": "user", "content": prompt}
                ]
            )

            texto = respuesta.choices[0].message.content
            st.success("Aquí tienes tus recomendaciones:")
            st.write(texto)

        except Exception as e:
            st.error("Ocurrió un error al consultar OpenAI.")
            st.text(str(e))

    if st.button("🔁 Volver a seleccionar"):
        st.session_state.paso = 2
        st.rerun()
