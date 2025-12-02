import streamlit as st
import os
from openai import OpenAI
import pandas as pd

# ============================
#   CONFIGURACIÓN GENERAL
# ============================
st.set_page_config(page_title="BiotechSuperfood IA", layout="wide")

# Cliente OpenAI (usa la variable de entorno / secret OPENAI_API_KEY)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ============================
#   ESTADO INICIAL
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

# ============================
#   CARGA DE TABLA DE COSTOS
# ============================
@st.cache_data
def load_cost_table():
    """
    Lee el Excel de precios de insumos y devuelve
    solo las columnas que nos interesan.
    - PROVEEDOR
    - insumos
    - Costo unitario (S/ por kg)
    """
    df = pd.read_excel("Precio de insumos.xlsx", header=1)  # ajusta ruta si está en /data
    df = df[["PROVEEDOR", "insumos", "Costo unitario"]].dropna()
    df = df.rename(columns={
        "PROVEEDOR": "proveedor",
        "insumos": "insumo",
        "Costo unitario": "costo_soles_kg"
    })
    return df

cost_df = load_cost_table()

# ============================
#      LOGIN
# ============================
if not st.session_state.logged_in:
    cols = st.columns([1, 3, 1])
    with cols[1]:
        st.markdown('<p class="title">¡Bienvenido a BiotechSuperfood IA!</p>', unsafe_allow_html=True)
        st.write("Ingrese sus credenciales para continuar:")

        user = st.text_input("Usuario")
        pwd = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if user == "Antonycomercial123@gmail.com" and pwd == "Form197@":
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

    col1, _ = st.columns(2)
    with col1:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 2}))
    st.stop()

# ============================
#  PASO 2 — CATEGORÍA PRODUCTO
# ============================
if st.session_state.paso == 2:
    st.markdown('<p class="step-title">Paso 2: Categoría del producto</p>', unsafe_allow_html=True)

    categorias = [
        "Mezcla en polvo",
        "Bebidas",
        "Snacks",
        "Suplementos nutricionales",
        "Productos lácteos",
        "Productos congelados",
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

    # --- Proteínas ---
    st.markdown('<p class="sub">Macronutrientes — Proteínas</p>', unsafe_allow_html=True)
    proteinas = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]
    seleccion_proteinas = []
    for p in proteinas:
        if st.checkbox(p):
            seleccion_proteinas.append(p)

    # Porcentaje de proteína (texto negro ya está cubierto por CSS)
    st.session_state.protein_pct = st.number_input(
        "Porcentaje de proteína (%)",
        min_value=0,
        max_value=90,
        step=1,
    )

    # --- Carbohidratos ---
    st.markdown('<p class="sub">Macronutrientes — Carbohidratos</p>', unsafe_allow_html=True)
    carbs = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"]
    seleccion_carbs = [c for c in carbs if st.checkbox(c, key=f"carb_{c}")]

    # --- Grasas ---
    st.markdown('<p class="sub">Macronutrientes — Grasas</p>', unsafe_allow_html=True)
    grasas = ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cañamo"]
    seleccion_grasas = [g for g in grasas if st.checkbox(g, key=f"grasa_{g}")]

    # --- Vitaminas ---
    st.markdown('<p class="sub">Micronutrientes — Vitaminas</p>', unsafe_allow_html=True)
    vitaminas = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    seleccion_vit = [v for v in vitaminas if st.checkbox(v, key=f"vit_{v}")]

    # --- Minerales ---
    st.markdown('<p class="sub">Micronutrientes — Minerales</p>', unsafe_allow_html=True)
    minerales = ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"]
    seleccion_min = []
    for m in minerales:
        if st.checkbox(m, key=f"min_{m}"):
            seleccion_min.append(m)

    # Porcentaje de hierro
    st.session_state.iron_pct = st.number_input(
        "Porcentaje de hierro (%)",
        min_value=0,
        max_value=90,
        step=1,
    )

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
#  PASO 4 — PARÁMETROS ORGANOLEPTICOS
# ============================
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

    # ============================
    #  FILTRAR TABLA DE COSTOS POR INGREDIENTES SELECCIONADOS
    # ============================
    seleccion = [ing.lower() for ing in st.session_state.ingredientes]

    costos_seleccionados = cost_df[
        cost_df["insumo"].str.lower().isin(seleccion)
    ].copy()

    # Construimos un texto tipo tabla para el prompt
    if not costos_seleccionados.empty:
        tabla_costos_text = "Insumo | Proveedor | Costo_soles_por_kg\n"
        for _, row in costos_seleccionados.iterrows():
            tabla_costos_text += f"{row['insumo']} | {row['proveedor']} | {row['costo_soles_kg']}\\n"
    else:
        tabla_costos_text = "NO SE ENCONTRARON PRECIOS PARA LOS INSUMOS SELECCIONADOS.\n"

    # ============================
    #  PROMPT POR DEFECTO A LA IA
    # ============================
    default_prompt = (
        f"Eres un experto formulador de alimentos.\n\n"
        f"Usa la siguiente información para proponer una formulación de un producto en polvo:\n\n"
        f"País: {st.session_state.pais}\n"
        f"Categoría de producto: {st.session_state.categoria}\n"
        f"Ingredientes seleccionados: {st.session_state.ingredientes}\n"
        f"Proteína requerida (%): {st.session_state.protein_pct}\n"
        f"Hierro requerido (%): {st.session_state.iron_pct}\n"
        f"Parámetros organolépticos: {st.session_state.organolepticos}\n\n"
        f"La siguiente tabla contiene los COSTOS UNITARIOS REALES (en soles por kg) "
        f"de cada insumo, por proveedor:\n\n"
        f"{tabla_costos_text}\n"
        f"Reglas importantes:\n"
        f"- Usa SOLO estos precios para calcular los costos de la formulación.\n"
        f"- Si algún ingrediente no aparece en la tabla, dilo explícitamente y no inventes su precio.\n"
        f"- Trabaja con un peso total de 100 g de producto final.\n\n"
        f"Tu salida debe incluir:\n"
        f"1) La formulación detallada (ingrediente, porcentaje, gramos en 100 g).\n"
        f"2) El costo estimado por 100 g, usando los precios de la tabla.\n"
        f"3) Costo estimado por kg.\n"
        f"4) Una tabla nutricional aproximada basada en la formulación.\n"
        f"5) Comentarios sobre qué proveedor conviene para cada insumo.\n"
    )

    prompt_input = st.text_area("Prompt enviado a la IA:", default_prompt, height=300)

    # ============================
    #  LLAMADA A OPENAI
    # ============================
    def call_ai(prompt: str):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un experto formulador de alimentos y analista de costos."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.3,
            )
            st.session_state.ai_response = response.choices[0].message.content
            st.session_state.paso = 5
        except Exception as e:
            st.error(f"Error al llamar a OpenAI: {e}")

    if st.button("Generar fórmula con IA"):
        with st.spinner("Generando formulación con IA..."):
            call_ai(prompt_input)

    st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 3}))

    st.stop()
    
# ============================
# PASO 5 — RESULTADOS FINALES
# ============================
if st.session_state.paso == 5:
    st.markdown('<p class="step-title">Resultados generados con IA</p>', unsafe_allow_html=True)

    if not st.session_state.ai_response:
        st.error("No se recibió ninguna respuesta de la IA.")
    else:
        st.markdown("### Respuesta detallada de la IA")
        st.write(st.session_state.ai_response)

    st.button("Volver al inicio", on_click=lambda: st.session_state.update({"paso": 1}))
