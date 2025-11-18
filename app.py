import streamlit as st
import os
from groq import Groq

# ============================
# CONFIGURACIÓN GENERAL
# ============================

st.set_page_config(page_title="BiotechSuperfood IA", layout="wide")

PRIMARY_COLOR = "#5947fd"
DARK_COLOR = "#1d1e1c"
TEXT_COLOR = "white"

# ============================
# CSS PREMIUM
# ============================

st.markdown(
    f"""
    <style>

    html, body, .main, .block-container {{
        background-color: {PRIMARY_COLOR} !important;
        color: {TEXT_COLOR} !important;
        font-family: 'Inter', sans-serif;
    }}

    /* CABECERA */
    .header-container {{
        width: 100%;
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 25px;
        background-color: rgba(25, 10, 100, 0.25);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255,255,255,0.25);
        position: sticky;
        top: 0;
        z-index: 999;
        border-radius: 0 0 18px 18px;
    }}

    img.header-logo {{
        height: 55px;
        border-radius: 12px;
        filter: drop-shadow(0px 0px 4px rgba(0,0,0,0.35));
    }}

    .header-title {{
        font-size: 30px;
        font-weight: 700;
        color: white !important;
    }}

    /* TARJETAS GLASS */
    .glass-card {{
        background: rgba(255, 255, 255, 0.10);
        backdrop-filter: blur(18px);
        padding: 30px;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.25);
        margin-top: 25px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    }}

    .step-title {{
        font-size: 28px;
        font-weight: 700;
        color: white !important;
        margin-bottom: 12px;
    }}

    .sub {{
        font-size: 20px;
        font-weight: 600;
        color: #e5e4ff !important;
    }}

    /* INPUTS */
    input, textarea, select {{
        background-color: {DARK_COLOR} !important;
        color: white !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        padding: 10px !important;
    }}

    /* CHECKBOXES AZULES */
    input[type=checkbox] {{
        accent-color: {PRIMARY_COLOR};
        width: 20px;
        height: 20px;
        margin-right: 8px;
    }}

    label {{
        color: white !important;
        font-size: 16px !important;
    }}

    /* BOTONES */
    .stButton > button {{
        background: {DARK_COLOR};
        border: 2px solid white;
        color: white;
        padding: 10px 20px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 17px;
        transition: 0.2s ease-in-out;
    }}

    .stButton > button:hover {{
        background: white !important;
        color: {PRIMARY_COLOR} !important;
        border: 2px solid {PRIMARY_COLOR};
        transform: translateY(-2px);
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================
# CABECERA CON LOGO
# ============================

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
# SESIÓN
# ============================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "paso" not in st.session_state:
    st.session_state.paso = 1

for key in ["pais", "categoria", "ingredientes", "micro_ingredientes",
            "protein_pct", "iron_pct", "organolepticos", "ai_response"]:
    if key not in st.session_state:
        st.session_state[key] = None if key != "ingredientes" else []

# ============================
# LOGIN
# ============================

if not st.session_state.logged_in:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<p class="step-title">¡Bienvenido a BiotechSuperfood IA!</p>', unsafe_allow_html=True)

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user == "admin" and pwd == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Credenciales incorrectas")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================
# PASO 1 — PAÍS
# ============================

if st.session_state.paso == 1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown('<p class="step-title">Paso 1: Selección de país</p>', unsafe_allow_html=True)
    st.session_state.pais = st.selectbox("Seleccione el país:", ["Perú", "Colombia", "México"])

    st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 2}))

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================
# PASO 2 — CATEGORÍA
# ============================

if st.session_state.paso == 2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

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

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================
# PASO 3 — INGREDIENTES
# ============================

if st.session_state.paso == 3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown('<p class="step-title">Paso 3: Selección de ingredientes</p>', unsafe_allow_html=True)

    # Proteínas
    st.markdown('<p class="sub">Macronutrientes — Proteínas</p>', unsafe_allow_html=True)
    proteinas = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]
    seleccion_proteinas = [p for p in proteinas if st.checkbox(p)]

    st.session_state.protein_pct = st.number_input("Porcentaje de proteína (%)", 0, 90, 0)

    # Carbohidratos
    st.markdown('<p class="sub">Macronutrientes — Carbohidratos</p>', unsafe_allow_html=True)
    carbs = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"]
    seleccion_carbs = [c for c in carbs if st.checkbox(c, key=f"carb_{c}")]

    # Grasas
    st.markdown('<p class="sub">Macronutrientes — Grasas</p>', unsafe_allow_html=True)
    grasas = ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cañamo"]
    seleccion_grasas = [g for g in grasas if st.checkbox(g, key=f"grasa_{g}")]

    # Vitaminas
    st.markdown('<p class="sub">Micronutrientes — Vitaminas</p>', unsafe_allow_html=True)
    vitaminas = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    seleccion_vit = [v for v in vitaminas if st.checkbox(v, key=f"vit_{v}")]

    # Minerales
    st.markdown('<p class="sub">Micronutrientes — Minerales</p>', unsafe_allow_html=True)
    minerales = ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"]
    seleccion_min = [m for m in minerales if st.checkbox(m, key=f"min_{m}")]

    st.session_state.iron_pct = st.number_input("Porcentaje de hierro (%)", 0, 90, 0)

    st.session_state.ingredientes = (
        seleccion_proteinas +
        seleccion_carbs +
        seleccion_grasas +
        seleccion_vit +
        seleccion_min
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 2}))
    with col2:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 4}))

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================
# PASO 4 — PARÁMETROS ORGANOLEPTICOS
# ============================

if st.session_state.paso == 4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

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

    default_prompt = (
        f"Genera una formulación nutricional completa usando los siguientes datos:\n\n"
        f"País: {st.session_state.pais}\n"
        f"Categoría: {st.session_state.categoria}\n"
        f"Ingredientes: {st.session_state.ingredientes}\n"
        f"Proteína requerida: {st.session_state.protein_pct}%\n"
        f"Hierro requerido: {st.session_state.iron_pct}%\n"
        f"Parámetros organolépticos: {st.session_state.organolepticos}\n\n"
        f"Devuelve formulación final, costo estimado y tabla nutricional."
    )

    prompt_input = st.text_area("Prompt enviado a la IA:", default_prompt, height=300)

    # === FUNCIÓN IA ===
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
            st.error(f"Error al llamar a Groq API:\n\n{str(e)}")

    # === BOTÓN GENERAR ===
    if st.button("Generar fórmula con IA"):
        with st.spinner("Generando formulación con Groq..."):
            call_ai(prompt_input)

    st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 3}))

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ============================
# PASO 5 — RESULTADO FINAL
# ============================

if st.session_state.paso == 5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.markdown('<p class="step-title">Resultados generados con IA</p>', unsafe_allow_html=True)

    if not st.session_state.ai_response:
        st.error("No se recibió respuesta de la IA.")
    else:
        st.write(st.session_state.ai_response)

    st.button("Volver al inicio", on_click=lambda: st.session_state.update({"paso": 1}))

    st.markdown('</div>', unsafe_allow_html=True)
