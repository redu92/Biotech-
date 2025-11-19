import streamlit as st
import os
from groq import Groq

# ==========================================
#   CONFIGURACIÓN GENERAL DE LA APP
# ==========================================
st.set_page_config(page_title="BiotechSuperfood IA", layout="wide")

# ==========================================
#   CSS PERSONALIZADO (DISEÑO COMPLETO)
# ==========================================
st.markdown("""
<style>

    /* ============================
       COLORES BASE
    ============================*/
    body, .main, .block-container {
        background-color: #5947fd !important;
    }

    /* ============================
       TIPOGRAFÍA GENERAL
    ============================*/
    * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* ============================
       INPUTS Y TEXTAREAS (texto negro)
    ============================*/
    input, textarea, select, div[role="textbox"] {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
    }

    /* ============================
       SELECTBOX — texto del select cerrado
    ============================*/
    div[data-baseweb="select"] > div {
        color: #ffffff !important;
        background-color: #5947fd !important;
    }

    /* ============================
       CHECKBOX Y RADIO
    ============================*/
    div[data-baseweb="checkbox"] > div {
        background-color: transparent !important;
        border: 2px solid #ffffff !important;
    }
    div[data-baseweb="checkbox"] svg,
    div[data-baseweb="radio"] svg {
        fill: #00a0ff !important;
    }

    /* ============================
       BOTONES
    ============================*/
    .stButton button {
        background-color: #1d1e1c !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        padding: 10px 18px !important;
        border: none !important;
    }
    .stButton button:hover {
        background-color: #000000 !important;
        transform: scale(1.02);
    }

    /* ============================
       CABECERA CON LOGO
    ============================*/
    .header-container {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 15px 20px;
        background-color: #1d1e1c;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 2px solid white;
    }
    .header-logo {
        height: 70px;
        border-radius: 8px;
    }
    .header-title {
        font-size: 32px;
        font-weight: 900 !important;
        color: white !important;
    }

    /* ===================================================
       FIX REAL Y DEFINITIVO PARA TU MENÚ DESPLEGABLE
       (Streamlit usa portales + clases Emotion)
    ====================================================*/

    /* Opciones reales del menú (clase Emotion detectada) */
    .st-emotion-cache-qiev7j,
    .st-emotion-cache-qiev7j * {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* Cualquier menú desplegable renderizado en un portal */
    div[role="dialog"] div[class*="st-emotion-cache"] {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
    }

</style>
""", unsafe_allow_html=True)
# ==========================================
#  HEADER CON LOGO — SIEMPRE VISIBLE
# ==========================================
st.markdown(
    f"""
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/redu92/Biotech-/main/logo%20biotech.jpg" class="header-logo">
        <div class="header-title">BiotechSuperfood IA</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
#   INICIALIZAR SESIÓN
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "paso" not in st.session_state:
    st.session_state.paso = 1

if "pais" not in st.session_state:
    st.session_state.pais = None

if "categoria" not in st.session_state:
    st.session_state.categoria = None

if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []

if "organolepticos" not in st.session_state:
    st.session_state.organolepticos = []

if "protein_pct" not in st.session_state:
    st.session_state.protein_pct = 0

if "iron_pct" not in st.session_state:
    st.session_state.iron_pct = 0

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None


# ==========================================
#         LOGIN
# ==========================================
if not st.session_state.logged_in:
    st.write("Ingrese sus credenciales para continuar:")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.stop()


# ==========================================
#   PASO 1 — PAÍS
# ==========================================
if st.session_state.paso == 1:
    st.header("Paso 1: Selección de país")

    st.session_state.pais = st.selectbox("Seleccione el país:", ["Perú", "Colombia", "México"])

    st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 2}))
    st.stop()


# ==========================================
#   PASO 2 — CATEGORÍA
# ==========================================
if st.session_state.paso == 2:
    st.header("Paso 2: Categoría del producto")

    categorias = [
        "Mezcla en polvo", "Bebidas", "Snacks",
        "Suplementos nutricionales", "Productos lácteos",
        "Productos congelados"
    ]

    st.session_state.categoria = st.radio("Seleccione una categoría:", categorias)

    col1, col2 = st.columns(2)
    col1.button("Atrás", on_click=lambda: st.session_state.update({"paso": 1}))
    col2.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 3}))
    st.stop()


# ==========================================
#   PASO 3 — INGREDIENTES
# ==========================================
if st.session_state.paso == 3:
    st.header("Paso 3: Selección de ingredientes")

    st.subheader("Proteínas (Macronutrientes)")
    proteinas = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]
    seleccion_proteinas = [p for p in proteinas if st.checkbox(p)]

    st.session_state.protein_pct = st.number_input("Porcentaje de proteína (%)", min_value=0, max_value=90)

    st.subheader("Carbohidratos")
    carbs = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"]
    seleccion_carbs = [c for c in carbs if st.checkbox(c, key=f"carb_{c}")]

    st.subheader("Grasas")
    grasas = ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cañamo"]
    seleccion_grasas = [g for g in grasas if st.checkbox(g, key=f"grasa_{g}")]

    st.subheader("Micronutrientes — Vitaminas")
    vitaminas = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    seleccion_vit = [v for v in vitaminas if st.checkbox(v, key=f"vit_{v}")]

    st.subheader("Micronutrientes — Minerales")
    minerales = ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"]
    seleccion_min = [m for m in minerales if st.checkbox(m, key=f"min_{m}")]

    st.session_state.iron_pct = st.number_input("Porcentaje de hierro (%)", min_value=0, max_value=90)

    st.session_state.ingredientes = (
        seleccion_proteinas + seleccion_carbs + seleccion_grasas + seleccion_vit + seleccion_min
    )

    col1, col2 = st.columns(2)
    col1.button("Atrás", on_click=lambda: st.session_state.update({"paso": 2}))
    col2.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 4}))
    st.stop()


# ==========================================
#  PASO 4 — PARÁMETROS ORGANOLEPTICOS
# ==========================================
if st.session_state.paso == 4:
    st.header("Paso 4: Parámetros organolépticos")

    saborizantes = ["Vainilla", "Cacao", "Frutos deshidratados", "Especias", "Menta", "Cítricos", "Café"]
    endulzantes = ["Eritritol (E968)", "Stevia (E960)", "Sucralosa"]
    estabilizantes = ["Goma Xantana", "Goma Guar", "Pectina", "Goma de Tara"]

    organo = []

    st.subheader("Saborizantes")
    for s in saborizantes:
        if st.checkbox(s, key=f"org_s_{s}"):
            organo.append(s)

    st.subheader("Endulzantes")
    for e in endulzantes:
        if st.checkbox(e, key=f"org_e_{e}"):
            organo.append(e)

    st.subheader("Estabilizantes")
    for e in estabilizantes:
        if st.checkbox(e, key=f"org_est_{e}"):
            organo.append(e)

    st.session_state.organolepticos = organo

    default_prompt = (
        f"Genera una formulación nutricional usando:\n\n"
        f"País: {st.session_state.pais}\n"
        f"Categoría: {st.session_state.categoria}\n"
        f"Ingredientes: {st.session_state.ingredientes}\n"
        f"Proteína (%): {st.session_state.protein_pct}\n"
        f"Hierro (%): {st.session_state.iron_pct}\n"
        f"Parámetros organolépticos: {st.session_state.organolepticos}\n\n"
        f"Devuelve: formulación final + tabla nutricional + costos estimados."
    )

    prompt_input = st.text_area("Prompt enviado a la IA:", default_prompt, height=300)


    # ---------------------------
    # Función para Groq
    # ---------------------------
    def call_ai(prompt):
        try:
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un experto formulador de alimentos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )

            st.session_state.ai_response = response.choices[0].message.content
            st.session_state.paso = 5

        except Exception as e:
            st.error(f"Error al llamar a la API de Groq:\n\n{str(e)}")


    if st.button("Generar fórmula con IA"):
        with st.spinner("Generando formulación con Groq..."):
            call_ai(prompt_input)

    st.stop()


# ==========================================
#  PASO 5 — RESULTADOS IA
# ==========================================
if st.session_state.paso == 5:
    st.header("Resultados generados con IA")

    if st.session_state.ai_response:
        st.write(st.session_state.ai_response)
    else:
        st.error("No se recibió respuesta de la IA.")

    st.button("Volver al inicio", on_click=lambda: st.session_state.update({"paso": 1}))
