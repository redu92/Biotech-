import streamlit as st
import os
from groq import Groq
import streamlit as st

# ============================
#      ESTILOS GLOBALes
# ============================
PRIMARY_COLOR = "#5947fd"     # Morado
DARK_COLOR = "#1d1e1c"        # Negro grisáceo
TEXT_COLOR = "white"

st.markdown(
    f"""
    <style>
        /* Fondo general */
        .main {{
            background-color: {PRIMARY_COLOR};
        }}

        /* Texto blanco general */
        body, p, div, label, span, h1, h2, h3, h4 {{
            color: {TEXT_COLOR} !important;
        }}

        /* Inputs */
        .stTextInput > div > div > input,
        .stTextArea textarea,
        .stSelectbox div div div {{
            background-color: {DARK_COLOR};
            color: white !important;
            border-radius: 8px;
        }}

        /* Checkboxes */
        .stCheckbox label {{
            color: {TEXT_COLOR} !important;
        }}

        /* Botones personalizados */
        .stButton > button {{
            background-color: {DARK_COLOR};
            color: white;
            border-radius: 10px;
            padding: 0.6rem 1rem;
            font-weight: bold;
            border: 2px solid white;
        }}

        .stButton > button:hover {{
            background-color: white;
            color: {PRIMARY_COLOR};
            border: 2px solid {PRIMARY_COLOR};
        }}

        /* Cabecera fija */
        .header-container {{
            width: 100%;
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 15px;
            background-color: {PRIMARY_COLOR};
            border-bottom: 3px solid {DARK_COLOR};
            position: sticky;
            top: 0;
            z-index: 999;
        }}

        .header-title {{
            font-size: 28px;
            font-weight: 700;
            color: white !important;
        }}

        img.header-logo {{
            height: 60px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
# ============================
# CABECERA DE LA APLICACIÓN
# ============================

# Ruta del logo en tu GitHub público
logo_url = "https://raw.githubusercontent.com/redu92/Biotech-/main/logo%20biotech.jpg"

st.markdown(
    f"""
    <div class="header-container">
        <img src="{logo_url}" class="header-logo">
        <span class="header-title">Biotech — Formulador Nutricional</span>
    </div>
    """,
    unsafe_allow_html=True
)
# ============================
#   CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(page_title="BiotechSuperfood IA", layout="wide")

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ============================
#   VARIABLES DE SESIÓN
# ============================
defaults = {
    "logged_in": False,
    "paso": 1,
    "pais": None,
    "categoria": None,
    "ingredientes": [],
    "micro_ingredientes": [],
    "protein_pct": 0,
    "iron_pct": 0,
    "organolepticos": [],
    "ai_response": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================
#       ESTILO (AZUL)
# ============================
st.markdown("""
<style>
    .title {
        color: #1A73E8;
        font-size: 32px;
        font-weight: bold;
    }
    .step-title {
        color: #1A73E8;
        font-size: 26px;
        font-weight: bold;
        margin-top: 20px;
    }
    .sub {
        color: #3282F6;
        font-size: 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


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
#    PASO 1 — PAÍS
# ============================
if st.session_state.paso == 1:

    st.markdown('<p class="step-title">Paso 1: Selección de país</p>', unsafe_allow_html=True)

    st.session_state.pais = st.selectbox("Seleccione el país:", ["Perú", "Colombia", "México"])

    if st.button("Siguiente"):
        st.session_state.paso = 2
        st.rerun()

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
        if st.button("Atrás"):
            st.session_state.paso = 1
            st.rerun()
    with col2:
        if st.button("Siguiente"):
            st.session_state.paso = 3
            st.rerun()

    st.stop()


# ============================
#   PASO 3 — INGREDIENTES
# ============================
if st.session_state.paso == 3:

    st.markdown('<p class="step-title">Paso 3: Selección de ingredientes</p>', unsafe_allow_html=True)

    # ---- PROTEÍNAS ----
    st.markdown('<p class="sub">Macronutrientes — Proteínas</p>', unsafe_allow_html=True)
    proteinas = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]

    seleccion_proteinas = []
    for p in proteinas:
        if st.checkbox(p, key=f"prot_{p}"):
            seleccion_proteinas.append(p)

    st.session_state.protein_pct = st.number_input(
        "Porcentaje de proteína (%)",
        min_value=0, max_value=90, step=1
    )

    # ---- CARBOHIDRATOS ----
    st.markdown('<p class="sub">Macronutrientes — Carbohidratos</p>', unsafe_allow_html=True)
    carbs = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"]
    seleccion_carbs = [c for c in carbs if st.checkbox(c, key=f"carb_{c}")]

    # ---- GRASAS ----
    st.markdown('<p class="sub">Macronutrientes — Grasas</p>', unsafe_allow_html=True)
    grasas = ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cañamo"]
    seleccion_grasas = [g for g in grasas if st.checkbox(g, key=f"grasa_{g}")]

    # ---- VITAMINAS ----
    st.markdown('<p class="sub">Micronutrientes — Vitaminas</p>', unsafe_allow_html=True)
    vitaminas = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    seleccion_vit = [v for v in vitaminas if st.checkbox(v, key=f"vit_{v}")]

    # ---- MINERALES ----
    st.markdown('<p class="sub">Micronutrientes — Minerales</p>', unsafe_allow_html=True)
    minerales = ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"]

    seleccion_min = []
    for m in minerales:
        if st.checkbox(m, key=f"min_{m}"):
            seleccion_min.append(m)

    st.session_state.iron_pct = st.number_input(
        "Porcentaje de hierro (%)",
        min_value=0, max_value=90, step=1
    )

    # Guardar ingredientes
    st.session_state.ingredientes = (
        seleccion_proteinas +
        seleccion_carbs +
        seleccion_grasas +
        seleccion_vit +
        seleccion_min
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 2
            st.rerun()

    with col2:
        if st.button("Siguiente"):
            st.session_state.paso = 4
            st.rerun()

    st.stop()


# ============================
# PASO 4 — PARÁMETROS ORGANOLEPTICOS
# ============================
if st.session_state.paso == 4:

    st.markdown("## Paso 4: Parámetros organolépticos")

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

    # ----- PROMPT AUTOMÁTICO -----
    default_prompt = (
        f"Genera una formulación nutricional completa usando los siguientes datos:\n\n"
        f"País: {st.session_state.pais}\n"
        f"Categoría: {st.session_state.categoria}\n"
        f"Ingredientes seleccionados: {st.session_state.ingredientes}\n"
        f"Proteína requerida (%): {st.session_state.protein_pct}\n"
        f"Hierro requerido (%): {st.session_state.iron_pct}\n"
        f"Parámetros organolépticos: {st.session_state.organolepticos}\n\n"
        f"Usa precios promedio del país seleccionado.\n"
        f"Devuelve formulación final, costo estimado y tabla nutricional."
    )

    prompt_input = st.text_area("Prompt enviado a la IA:", default_prompt, height=300)

    # ----- FUNCIÓN GROQ -----
    def call_ai(prompt):
        try:
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
            st.rerun()

        except Exception as e:
            st.error(f"Error al llamar a Groq API:\n\n{str(e)}")

    # BOTÓN
    if st.button("Generar fórmula con IA"):
        with st.spinner("Generando formulación con Groq..."):
            call_ai(prompt_input)

    if st.button("Atrás"):
        st.session_state.paso = 3
        st.rerun()

    st.stop()


# ============================
# PASO 5 — RESULTADOS FINALES
# ============================
if st.session_state.paso == 5:

    st.markdown("## Resultados generados con IA")

    if st.session_state.ai_response is None:
        st.error("No se recibió ninguna respuesta de la IA.")
    else:
        st.markdown("### Respuesta detallada de la IA")
        st.write(st.session_state.ai_response)



    if st.button("Volver al inicio"):
        st.session_state.paso = 1
        st.rerun()
