import streamlit as st
import os
from groq import Groq

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================
#   CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(page_title="BiotechSuperfood IA", layout="wide")

# ============================
#       ESTADO DE SESIÓN
# ============================
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


# ============================
#       ESTILO GLOBAL
# ============================

st.markdown("""
<style>

    /* ======= FUENTES ======= */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
        color: white !important;
    }

    /* ======= FONDO GENERAL ======= */
    body {
        background-color: #5947fd !important;
    }
    .main {
        background-color: #5947fd !important;
    }

    /* ======= TÍTULOS ======= */
    .title {
        color: white !important;
        font-size: 34px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
    }

    .step-title {
        color: white !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        margin-top: 20px !important;
        margin-bottom: 10px !important;
    }

    .sub {
        color: white !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }

    label, .stRadio label, .stCheckbox label {
        color: white !important;
        font-size: 20px !important;
        font-weight: 700 !important;
    }

    /* ======= BOTONES ======= */
    .stButton>button {
        background-color: #1d1e1c !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        border: 2px solid white !important;
    }

    .stButton>button:hover {
        background-color: white !important;
        color: #1d1e1c !important;
        border: 2px solid #1d1e1c !important;
    }

    /* ======= INPUTS ======= */
    .stTextInput input, .stNumberInput input, textarea {
        background-color: #1d1e1c !important;
        color: white !important;
        border-radius: 8px !important;
        border: 2px solid white !important;
    }

    /* ======= CHECKBOX Y RADIO ESTILIZADOS ======= */
    input[type="checkbox"], input[type="radio"] {
        position: absolute;
        opacity: 0;
    }

    .stCheckbox label::before, .stRadio label::before {
        content: "";
        display: inline-block;
        width: 20px;
        height: 20px;
        margin-right: 10px;
        border: 2px solid white;
        background-color: white;
        border-radius: 4px;
        vertical-align: middle;
    }

    input[type="checkbox"]:checked + label::before,
    input[type="radio"]:checked + label::before {
        background-color: #5947fd !important;
        border: 2px solid white !important;
        background-image: url("data:image/svg+xml;utf8,<svg fill='white' viewBox='0 0 16 16' xmlns='http://www.w3.org/2000/svg'><path d='M12.97 4.97a.75.75 0 0 0-1.06-1.06L6.5 9.31 4.09 6.91a.75.75 0 1 0-1.06 1.06l3 3a.75.75 0 0 0 1.06 0l6-6z'/></svg>");
        background-repeat: no-repeat;
        background-position: center;
    }

    /* ======= LOGO EN CABECERA ======= */
    .header-logo {
        width: 180px;
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 20px;
    }

</style>
""", unsafe_allow_html=True)


# ======= LOGO SUPERIOR =======
st.image(
    "https://raw.githubusercontent.com/redu92/Biotech-/main/logo%20biotech.jpg",
    width=180
)


# ============================
#      LOGIN
# ============================
if not st.session_state.logged_in:
    st.markdown('<p class="title">¡Bienvenido a BiotechSuperfood IA!</p>', unsafe_allow_html=True)
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


# ============================
#      PASO 1 — PAÍS
# ============================
if st.session_state.paso == 1:
    st.markdown('<p class="step-title">Paso 1: Selección de país</p>', unsafe_allow_html=True)

    st.session_state.pais = st.selectbox("Seleccione el país:", ["Perú", "Colombia", "México"])

    st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 2}))
    st.stop()


# ============================
#  PASO 2 — CATEGORÍA PRODUCTO
# ============================
if st.session_state.paso == 2:
    st.markdown('<p class="step-title">Paso 2: Categoría del producto</p>', unsafe_allow_html=True)

    categorias = [
        "Mezcla en polvo", "Bebidas", "Snacks",
        "Suplementos nutricionales", "Productos lácteos",
        "Productos congelados"
    ]

    st.session_state.categoria = st.radio("Seleccione una categoría:", categorias)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 1}))
    with col2:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 3}))
    st.stop()


# ============================
#   PASO 3 — INGREDIENTES
# ============================
if st.session_state.paso == 3:
    st.markdown('<p class="step-title">Paso 3: Selección de ingredientes</p>', unsafe_allow_html=True)

    st.markdown('<p class="sub">Macronutrientes — Proteínas</p>', unsafe_allow_html=True)
    proteinas = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]
    seleccion_proteinas = [p for p in proteinas if st.checkbox(p)]

    st.session_state.protein_pct = st.number_input("Porcentaje de proteína (%)", min_value=0, max_value=90)

    st.markdown('<p class="sub">Macronutrientes — Carbohidratos</p>', unsafe_allow_html=True)
    carbs = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"]
    seleccion_carbs = [c for c in carbs if st.checkbox(c, key=f"carb_{c}")]

    st.markdown('<p class="sub">Macronutrientes — Grasas</p>', unsafe_allow_html=True)
    grasas = ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cañamo"]
    seleccion_grasas = [g for g in grasas if st.checkbox(g, key=f"grasa_{g}")]

    st.markdown('<p class="sub">Micronutrientes — Vitaminas</p>', unsafe_allow_html=True)
    vitaminas = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    seleccion_vit = [v for v in vitaminas if st.checkbox(v, key=f"vit_{v}")]

    st.markdown('<p class="sub">Micronutrientes — Minerales</p>', unsafe_allow_html=True)
    minerales = ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"]
    seleccion_min = [m for m in minerales if st.checkbox(m, key=f"min_{m}")]

    st.session_state.iron_pct = st.number_input("Porcentaje de hierro (%)", min_value=0, max_value=90)

    st.session_state.ingredientes = (
        seleccion_proteinas + seleccion_carbs + seleccion_grasas + seleccion_vit + seleccion_min
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 2}))
    with col2:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 4}))
    st.stop()


# ============================
# PASO 4 — PARÁMETROS ORGANOLEPTICOS
# ============================
if st.session_state.paso == 4:
    st.markdown('<p class="step-title">Paso 4: Parámetros organolépticos</p>', unsafe_allow_html=True)

    saborizantes = ["Vainilla", "Cacao", "Frutos deshidratados", "Especias", "Menta", "Cítricos", "Café"]
    endulzantes = ["Eritritol (E968)", "Stevia (E960)", "Sucralosa"]
    estabilizantes = ["Goma Xantana", "Goma Guar", "Pectina", "Goma de Tara"]

    organo = []

    st.markdown("### Saborizantes")
    for s in saborizantes:
        if st.checkbox(s, key=f"org_s_{s}"):
            organo.append(s)

    st.markdown("### Endulzantes")
    for e in endulzantes:
        if st.checkbox(e, key=f"org_e_{e}"):
            organo.append(e)

    st.markdown("### Estabilizantes")
    for e in estabilizantes:
        if st.checkbox(e, key=f"org_est_{e}"):
            organo.append(e)

    st.session_state.organolepticos = organo

    prompt = (
        f"Genera una formulación nutricional completa usando:\n"
        f"País: {st.session_state.pais}\n"
        f"Categoría: {st.session_state.categoria}\n"
        f"Ingredientes: {st.session_state.ingredientes}\n"
        f"Proteína requerida (%): {st.session_state.protein_pct}\n"
        f"Hierro requerido (%): {st.session_state.iron_pct}\n"
        f"Parámetros organolépticos: {st.session_state.organolepticos}\n"
        f"Usa precios del país y devuelve formulación final, costos y tabla nutricional."
    )

    st.write("### Prompt enviado a la IA:")
    prompt_input = st.text_area("", prompt, height=300)


    # ========== FUNCIÓN IA ==========
    def call_ai(prompt):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "Eres un experto formulador de alimentos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1800,
                temperature=0.3
            )

            st.session_state.ai_response = response.choices[0].message.content
            st.session_state.paso = 5

        except Exception as e:
            st.error(f"Error al llamar a Groq API:\n\n{str(e)}")


    # Botón IA
    if st.button("Generar fórmula con IA"):
        with st.spinner("Generando formulación con Groq..."):
            call_ai(prompt_input)

    st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 3}))

    st.stop()


# ============================
# PASO 5 — RESULTADOS
# ============================
if st.session_state.paso == 5:
    st.markdown('<p class="step-title">Resultados generados con IA</p>', unsafe_allow_html=True)

    if not st.session_state.ai_response:
        st.error("No se recibió respuesta de la IA.")
    else:
        st.write(st.session_state.ai_response)

    st.button("Volver al inicio", on_click=lambda: st.session_state.update({"paso": 1}))
