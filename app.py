import streamlit as st
from groq import Groq

# ------------------------------
#   CONFIGURACIÓN DE PÁGINA
# ------------------------------
st.set_page_config(
    page_title="Biotech Prompt Generator",
    page_icon="🧬",
    layout="wide"
)

# ------------------------------
#   ESTILOS CSS PERSONALIZADOS
# ------------------------------
custom_css = """
<style>

    /* Fondo general */
    html, body, [class*="stApp"] {
        background-color: #5947fd !important;
    }

    /* Títulos y textos */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* Selectores (radio-buttons) */
    div.stRadio > label {
        color: white !important;
        font-weight: 800 !important;
    }

    /* Texto de las opciones */
    div.stRadio > div[role='radiogroup'] label {
        color: white !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
    }

    /* Ocultamos el radio button original */
    div[role='radiogroup'] > div > div:first-child {
        visibility: hidden;
        height: 0px;
        width: 0px;
    }

    /* Reemplazo por cuadrado blanco */
    div[role='radiogroup'] > div {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    div[role='radiogroup'] > div:before {
        content: "";
        height: 20px;
        width: 20px;
        border-radius: 4px;
        background-color: white;
        border: 2px solid white;
        display: inline-block;
    }

    /* Cuando está seleccionado → aparece check azul */
    div[role='radiogroup'] > div[aria-checked="true"]:before {
        background-color: #ffffff;
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/2/27/White_check.svg');
        background-size: 20px 20px;
        background-repeat: no-repeat;
        background-position: center;
        border: 2px solid #00aaff;
    }

    /* Botones */
    .stButton>button {
        background-color: #1d1e1c !important;
        color: white !important;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 800;
        border: 2px solid white;
        font-size: 1.1rem;
    }

    /* Caja de texto */
    textarea, input {
        background-color: #1d1e1c !important;
        color: white !important;
        font-weight: 600 !important;
        border: 2px solid #ffffff !important;
    }

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ------------------------------
#   LOGO DEL GITHUB
# ------------------------------
logo_url = "https://raw.githubusercontent.com/redu92/Biotech-/main/logo%20biotech.jpg"

st.image(logo_url, width=180)
st.title("Generador de Prompts - Biotech 🧬")


# ------------------------------
#   FUNCIÓN PARA CONSULTAR GROQ
# ------------------------------
def call_ai(prompt):
    try:
        client = Groq(api_key=st.session_state["api_key"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error al llamar a Groq API:\n\n{e}"


# ------------------------------
#   VARIABLES DE SESIÓN
# ------------------------------
if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "step" not in st.session_state:
    st.session_state.step = 1

if "category" not in st.session_state:
    st.session_state.category = None

if "final_prompt" not in st.session_state:
    st.session_state.final_prompt = ""


# ------------------------------
#           PASO 1
# ------------------------------
if st.session_state.step == 1:
    st.subheader("🔑 Ingresa tu API Key de Groq")
    st.session_state.api_key = st.text_input("API Key:", type="password")

    if st.button("Continuar ➜"):
        if st.session_state.api_key.strip() == "":
            st.error("Debe ingresar una API Key válida.")
        else:
            st.session_state.step = 2
            st.rerun()


# ------------------------------
#           PASO 2
# ------------------------------
elif st.session_state.step == 2:
    st.subheader("📌 Selecciona la categoría del prompt")

    categories = [
        "🍎 Alimentación",
        "🌱 Agricultura",
        "🧪 Biotecnología",
        "🌾 Cultivos",
        "📊 Estadísticas",
        "📷 Generación de Imágenes",
    ]

    st.session_state.category = st.radio("Selecciona una opción:", categories)

    if st.button("Continuar ➜"):
        st.session_state.step = 3
        st.rerun()


# ------------------------------
#           PASO 3
# ------------------------------
elif st.session_state.step == 3:
    st.subheader("✍️ Describe brevemente qué deseas crear")

    user_input = st.text_area("Escribe tu idea aquí:", height=150)

    if st.button("Generar Prompt"):
        if user_input.strip() == "":
            st.error("Debe ingresar una descripción.")
        else:
            full_prompt = (
                f"Genera un prompt altamente optimizado para IA, claro, profesional y detallado. "
                f"La categoría es: {st.session_state.category}. "
                f"Descripción del usuario: {user_input}"
            )

            st.session_state.final_prompt = call_ai(full_prompt)
            st.session_state.step = 4
            st.rerun()


# ------------------------------
#           PASO 4 — Resultado
# ------------------------------
elif st.session_state.step == 4:
    st.subheader("🎉 Tu prompt está listo")

    st.text_area("Prompt generado:", st.session_state.final_prompt, height=250)

    st.success("¡Prompt generado con éxito!")

    if st.button("Generar otro prompt"):
        st.session_state.step = 2
        st.rerun()
