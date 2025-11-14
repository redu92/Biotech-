import streamlit as st
import os
from openai import OpenAI

# ============================
#   CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(page_title="BiotechSuperfood IA", layout="wide")

# Inicializar sesión
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

if "micro_ingredientes" not in st.session_state:
    st.session_state.micro_ingredientes = []

if "protein_pct" not in st.session_state:
    st.session_state.protein_pct = 0

if "iron_pct" not in st.session_state:
    st.session_state.iron_pct = 0

if "organolepticos" not in st.session_state:
    st.session_state.organolepticos = []

if "ai_response" not in st.session_state:
    st.session_state.ai_response = None


# ============================
#       ESTILO AZUL
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
#      PASO 1 — PAÍS
# ============================
if st.session_state.paso == 1:
    st.markdown('<p class="step-title">Paso 1: Selección de país</p>', unsafe_allow_html=True)

    st.session_state.pais = st.selectbox("Seleccione el país:", ["Perú", "Colombia", "México"])

    col1, col2 = st.columns(2)
    with col1:
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
    seleccion_proteinas = []
    for p in proteinas:
        if st.checkbox(p):
            seleccion_proteinas.append(p)

    st.session_state.protein_pct = st.number_input(
        "Porcentaje de proteína (%)",
        min_value=0, max_value=90, step=1
    )

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
    seleccion_min = []
    for m in minerales:
        if st.checkbox(m, key=f"min_{m}"):
            seleccion_min.append(m)

    st.session_state.iron_pct = st.number_input(
        "Porcentaje de hierro (%)",
        min_value=0, max_value=90, step=1
    )

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

    st.markdown("### Prompt a enviar a la IA")
    default_prompt = (
        f"Genera una formulación con todos los ítems seleccionados previamente:\n\n"
        f"País: {st.session_state.pais}\n"
        f"Categoría: {st.session_state.categoria}\n"
        f"Ingredientes: {st.session_state.ingredientes}\n"
        f"Proteína (%): {st.session_state.protein_pct}\n"
        f"Hierro (%): {st.session_state.iron_pct}\n"
        f"Parámetros organolépticos: {st.session_state.organolepticos}\n\n"
        f"Usa costos promedio y disponibilidad del país seleccionado. "
        f"Devuelve una formulación, costos estimados y una tabla nutricional clara."
    )

    if "prompt_openai" not in st.session_state:
        st.session_state.prompt_openai = default_prompt

    st.session_state.prompt_openai = st.text_area(
        "Prompt enviado a la IA:", 
        st.session_state.prompt_openai
    )

    def call_openai():
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": st.session_state.prompt_openai}]
            )
            st.session_state.ai_response = response.choices[0].message.content
            st.session_state.paso = 5
        except Exception as e:
            st.error(f"Error al llamar a OpenAI: {e}")

    if st.button("Generar fórmula integrada con IA"):
        with st.spinner("Generando fórmula..."):
            call_openai()
        st.rerun()

    st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 3}))
    st.stop()


# ============================
# PASO 5 — RESULTADOS FINALES
# ============================
if st.session_state.paso == 5:
    st.markdown('<p class="step-title">Resultados generados con IA</p>', unsafe_allow_html=True)

    st.subheader("Respuesta de la IA")
    st.markdown(st.session_state.get("ai_response", "_No hay respuesta disponible_"))

    st.subheader("Parámetros fijos del producto")
    st.info("""
    - Costo estimado: **8.00 soles**
    - Peso total: **100 g**
    - Porciones: **28**
    - Tamaño por porción: **3.5 g**
    """)

    st.button("Volver al inicio", on_click=lambda: st.session_state.update({"paso": 1}))

