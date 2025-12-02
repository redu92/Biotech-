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

if "fat_pct" not in st.session_state:
    st.session_state.fat_pct = 0

if "carb_pct" not in st.session_state:
    st.session_state.carb_pct = 0

if "fiber_pct" not in st.session_state:
    st.session_state.fiber_pct = 0

if "organolepticos" not in st.session_state:
    st.session_state.organolepticos = []

# NUEVO: porción y costo objetivo
if "porcion_g" not in st.session_state:
    st.session_state.porcion_g = 30  # gramos por defecto

if "costo_objetivo_kg" not in st.session_state:
    st.session_state.costo_objetivo_kg = 0.0

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

    /* Opciones reales de algunos menús desplegables (portales de Streamlit) */
    .st-emotion-cache-qiev7j,
    .st-emotion-cache-qiev7j * {
        color: #000000 !important;
        background-color: #ffffff !important;
        font-weight: 700 !important;
    }

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
    """
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
    """
    # Ajusta el nombre del archivo si es necesario
    df = pd.read_excel("Precio de insumos.xlsx", header=1)
    df = df[["PROVEEDOR", "insumos", "Costo unitario"]].dropna()
    df = df.rename(columns={
        "PROVEEDOR": "proveedor",
        "insumos": "insumo",
        "Costo unitario": "costo_soles_kg"
    })
    df["insumo_norm"] = df["insumo"].astype(str).str.strip().str.lower()
    return df

cost_df = load_cost_table()

def obtener_precio_desde_excel(nombre_ingrediente: str):
    """
    Devuelve (precio_kg, fuente) donde:
      - precio_kg es un float en soles/kg si se encontró en el Excel
      - fuente es 'tabla' si viene del Excel, o 'estimado' si no se encontró
    """
    if cost_df is None or cost_df.empty:
        return None, "estimado"

    nombre_norm = nombre_ingrediente.strip().lower()

    try:
        coincidencias = cost_df[cost_df["insumo_norm"] == nombre_norm]
    except Exception:
        return None, "estimado"

    if not coincidencias.empty:
        try:
            precio = float(coincidencias["costo_soles_kg"].iloc[0])
            return precio, "tabla"
        except Exception:
            return None, "estimado"

    return None, "estimado"

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

    # Solo Perú puede avanzar. Colombia y México muestran "Próximamente".
    if st.session_state.pais == "Perú":
        col1, _ = st.columns(2)
        with col1:
            st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 2}))
    else:
        st.markdown(
            """
            <div style="text-align:center; margin-top:40px;">
                <span style="font-size:32px; font-weight:900;">
                    Próximamente
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.stop()

# ============================
#  PASO 2 — CATEGORÍA PRODUCTO
# ============================
if st.session_state.paso == 2:
    st.markdown('<p class="step-title">Paso 2: Categoría del producto</p>', unsafe_allow_html=True)

    # Solo se puede elegir "Mezcla en polvo"
    st.session_state.categoria = st.radio(
        "Seleccione una categoría (actualmente solo disponible Mezcla en polvo):",
        ["Mezcla en polvo"],
        index=0
    )

    # Mostrar las otras categorías como texto informativo "Próximamente"
    st.markdown("""
    **Otras categorías (no disponibles aún):**
    - Bebidas (Próximamente)
    - Snacks (Próximamente)
    - Suplementos nutricionales (Próximamente)
    - Productos lácteos (Próximamente)
    - Productos congelados (Próximamente)
    """)

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

    ingredientes_seleccionados = []

    # ===== Fuentes de proteínas =====
    st.markdown("### Fuentes de proteínas")
    prot_opts = [
        "Proteína de arveja",
        "Proteína suero de leche",
        "Proteína aislada de arroz",
        "Proteína de colágeno hidrolizado",
        "Calostro bovino",
    ]
    for p in prot_opts:
        if st.checkbox(p, key=f"prot_{p}"):
            ingredientes_seleccionados.append(p)

    st.session_state.protein_pct = st.number_input(
        "Porcentaje de proteína (%)",
        min_value=0,
        max_value=90,
        step=1,
    )

    # ===== Fuentes de grasas =====
    st.markdown("### Fuentes de grasas")
    fat_opts = [
        "Aceite de coco en polvo",
        "Aceite de girasol en polvo",
        "ARA",
        "DHA (Omega-3)",
        "Lecitina de soya en polvo",
    ]
    for g in fat_opts:
        if st.checkbox(g, key=f"fat_{g}"):
            ingredientes_seleccionados.append(g)

    st.session_state.fat_pct = st.number_input(
        "Porcentaje de grasas (%)",
        min_value=0,
        max_value=90,
        step=1,
    )

    # ===== Fuentes de carbohidratos / Superalimentos =====
    st.markdown("### Fuentes de carbohidratos - Selección de Superalimentos")
    carb_opts = [
        "Algarrobo en polvo",
        "Arándano rojo",
        "Banano verde en polvo",
        "Betaglucano 70%",
        "Cacao en polvo",
        "Café instantáneo",
        "Camu camu atomizado",
        "Espirulina",
        "Extracto de ciruela",
        "Extracto de limón",
        "Extracto de manzanilla",
        "Extracto de naranja",
        "Extracto de naranja agria",
        "Extracto de tamarindo",
        "Extracto de té verde 40%",
        "Extracto de Zen",
        "Ganoderma",
        "Garcinia cambogia",
        "Maca en polvo",
        "Quinua en polvo",
        "Yacón en polvo",
        "Curcumina (extracto de cúrcuma)",
    ]
    for c in carb_opts:
        if st.checkbox(c, key=f"carb_{c}"):
            ingredientes_seleccionados.append(c)

    st.session_state.carb_pct = st.number_input(
        "Porcentaje de carbohidrato (%)",
        min_value=0,
        max_value=90,
        step=1,
    )

    # ===== Micronutrientes - Vitaminas =====
    st.markdown("### Selección de Micronutrientes - Vitaminas")
    vit_opts = [
        "Vitamina A",
        "Vitamina C (ácido ascórbico)",
        "Vitamina D",
        "Vitamina E",
        "Vitamina K",
        "Mix Vitaminas del complejo B (B1, B2, B3, B5, B6, B7, B9, B12)",
        "Vitamina B1",
        "Vitamina B6",
        "Vitamina B12",
        "Mix vitamínico GK02",
    ]
    for v in vit_opts:
        if st.checkbox(v, key=f"vit_{v}"):
            ingredientes_seleccionados.append(v)

    # ===== Micronutrientes - Minerales =====
    st.markdown("### Selección de Micronutrientes - Minerales")
    min_opts = [
        "Hierro (bisglicinato ferroso)",
        "Hierro (lactoferrina)",
        "Carbonato de calcio",
        "Fosfato tricálcico",
        "Citrato de magnesio",
        "Citrato de potasio",
        "Glicinato de zinc",
    ]
    for m in min_opts:
        if st.checkbox(m, key=f"min_{m}"):
            ingredientes_seleccionados.append(m)

    # ===== Aminoácidos =====
    st.markdown("### Selección de Aminoácidos")
    amino_opts = [
        "Triptófano",
        "L-Carnitina",
        "L-Glutamina",
        "L-Glicina",
        "L-Taurina",
        "L-Cisteína",
        "L-Metionina",
        "L-Arginina",
    ]
    for a in amino_opts:
        if st.checkbox(a, key=f"amino_{a}"):
            ingredientes_seleccionados.append(a)

    # ===== Prebióticos =====
    st.markdown("### Selección de Prebióticos")
    pre_opts = [
        "Polidextrosa",
        "FOS",
        "Inulina",
    ]
    for pre in pre_opts:
        if st.checkbox(pre, key=f"pre_{pre}"):
            ingredientes_seleccionados.append(pre)

    st.session_state.fiber_pct = st.number_input(
        "Porcentaje de fibra (%)",
        min_value=0,
        max_value=90,
        step=1,
    )

    # ===== Probióticos =====
    st.markdown("### Selección de Probióticos")
    probio_opts = [
        "Bacillus coagulans SNZ1969",
        "Lactobacillus acidophilus LA-G80",
        "Bifidobacterium bifidum BB-G90",
        "Bifidobacterium longum subsp. longum BL-G301",
        "Lactiplantibacillus plantarum ZJUF T34",
        "Lactiplantibacillus plantarum Lp-G18",
        "Lactiplantibacillus plantarum YS1",
    ]
    for pr in probio_opts:
        if st.checkbox(pr, key=f"probio_{pr}"):
            ingredientes_seleccionados.append(pr)

    # Guardamos todos los ingredientes seleccionados
    st.session_state.ingredientes = ingredientes_seleccionados

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

    # ===== Saborizantes =====
    st.subheader("Saborizantes")
    saborizantes = [
        "Sabor a cereza",
        "Sabor arándano",
        "Sabor cereza",
        "Sabor fresa",
        "Sabor frutos rojos",
        "Sabor leche",
        "Sabor limón",
        "Sabor menta",
        "Sabor naranja",
        "Sabor vainilla",
    ]

    organo = []
    for s in saborizantes:
        if st.checkbox(s, key=f"sabor_{s}"):
            organo.append(s)

    # ===== Estabilizantes =====
    st.subheader("Estabilizantes")
    estabilizantes = ["Goma Xantana", "Goma Guar", "Pectina", "Goma de Tara"]
    for e in estabilizantes:
        if st.checkbox(e, key=f"estab_{e}"):
            organo.append(e)

    st.session_state.organolepticos = organo

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 3}))
    with col2:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 5}))
    st.stop()

# ============================
#  PASO 5 — PORCIÓN POR SERVICIO
# ============================
if st.session_state.paso == 5:
    st.header("Paso 5: Colocar la cantidad de porción por servicio")

    st.session_state.porcion_g = st.number_input(
        "Cantidad de gramos por porción (g):",
        min_value=1,
        max_value=500,
        value=st.session_state.porcion_g,
        step=1,
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 4}))
    with col2:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 6}))
    st.stop()

# ============================
#  PASO 6 — COSTO OBJETIVO POR KG
# ============================
if st.session_state.paso == 6:
    st.header("Paso 6: Colocar el costo objetivo por kilogramo de la formulación")

    st.session_state.costo_objetivo_kg = st.number_input(
        "Costo objetivo por kilogramo de la formulación (S/ por kg):",
        min_value=0.0,
        max_value=1000.0,
        value=float(st.session_state.costo_objetivo_kg),
        step=0.1,
        format="%.2f",
    )

    st.markdown(
        "Este será el costo máximo objetivo que deberá tener tu formulación. "
        "La IA deberá priorizar cumplir este costo ajustando los ingredientes."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", on_click=lambda: st.session_state.update({"paso": 5}))
    with col2:
        st.button("Siguiente", on_click=lambda: st.session_state.update({"paso": 7}))
    st.stop()

# ============================
# PASO 7 — PROMPT Y RESULTADOS FINALES
# ============================
if st.session_state.paso == 7:
    st.markdown('<p class="step-title">Paso 7: Generar formulación y resultados con IA</p>', unsafe_allow_html=True)

    # ------------------------------------
    # Construir texto de costos por ingrediente
    # ------------------------------------
    lineas_costos = []
    for ing in st.session_state.ingredientes:
        precio, fuente = obtener_precio_desde_excel(ing)
        if precio is not None and fuente == "tabla":
            lineas_costos.append(
                f"- {ing}: {precio:.2f} soles/kg (precio real desde la tabla de proveedores)."
            )
        else:
            lineas_costos.append(
                f"- {ing}: precio por kg NO está en la tabla; "
                f"por favor estima un precio de mercado realista en {st.session_state.pais}."
            )

    texto_costos = "\n".join(lineas_costos)

    # ------------------------------------
    # Construir sección de macronutrientes solo si el usuario los definió
    # ------------------------------------
    macros_texto = []
    if st.session_state.protein_pct > 0:
        macros_texto.append(f"Proteína requerida (%): {st.session_state.protein_pct}")
    if st.session_state.fat_pct > 0:
        macros_texto.append(f"Grasas requeridas (%): {st.session_state.fat_pct}")
    if st.session_state.carb_pct > 0:
        macros_texto.append(f"Carbohidratos requeridos (%): {st.session_state.carb_pct}")
    if st.session_state.fiber_pct > 0:
        macros_texto.append(f"Fibra requerida (%): {st.session_state.fiber_pct}")

    if macros_texto:
        texto_macros = "\n".join(macros_texto)
        instruccion_macros = (
            "Respeta estos porcentajes aproximados de macronutrientes en la formulación.\n"
        )
    else:
        texto_macros = "No se especificaron porcentajes de macronutrientes.\n"
        instruccion_macros = (
            "Como no se especificaron porcentajes de proteína, grasas, carbohidratos o fibra, "
            "propón tú una distribución adecuada de macronutrientes para este tipo de producto.\n"
        )

    # ------------------------------------
    # Prompt automático para la IA
    # ------------------------------------
    default_prompt = (
        f"Genera una formulación nutricional completa usando los siguientes datos:\n\n"
        f"País objetivo: {st.session_state.pais}\n"
        f"Categoría del producto: {st.session_state.categoria}\n"
        f"Ingredientes seleccionados (procura usarlos todos, salvo que alguno haga imposible cumplir el costo objetivo):\n"
        f"{st.session_state.ingredientes}\n\n"
        f"{texto_macros}"
        f"{instruccion_macros}\n"
        f"Parámetros organolépticos (saborizantes y estabilizantes): {st.session_state.organolepticos}\n"
        f"Tamaño de porción objetivo: {st.session_state.porcion_g} g por servicio.\n"
        f"Costo objetivo de la formulación: {st.session_state.costo_objetivo_kg:.2f} soles/kg (este es el costo MÁXIMO que debes priorizar cumplir).\n\n"
        f"Información de costos reales o a estimar (soles por kg):\n"
        f"{texto_costos}\n\n"
        f"Si el precio de algún ingrediente está marcado como estimado, "
        f"elige un valor razonable según el mercado actual para {st.session_state.pais}.\n\n"
        f"Objetivo principal: prioriza que el costo final por kg de la formulación sea menor o igual a "
        f"{st.session_state.costo_objetivo_kg:.2f} soles/kg. Ajusta las proporciones, especialmente de los ingredientes más caros, "
        f"para lograrlo sin sacrificar demasiado el perfil nutricional.\n\n"
        f"Con toda esta información, devuelve:\n"
        f"1) Una formulación final en forma de tabla (lista de ingredientes con porcentaje en la mezcla para 100 g).\n"
        f"2) El costo total estimado por 100 g, por porción de {st.session_state.porcion_g} g y por kg.\n"
        f"3) Una tabla nutricional aproximada por 100 g y por porción de {st.session_state.porcion_g} g.\n"
        f"4) Una breve explicación de por qué seleccionaste esa formulación, "
        f"teniendo en cuenta costo, disponibilidad, perfil nutricional y el costo objetivo.\n"
        f"5) Si no es posible cumplir exactamente el costo objetivo, indica el costo resultante y explica brevemente por qué."
    )

    prompt_input = st.text_area("Prompt enviado a la IA:", default_prompt, height=280)

    # ---------- llamada a OpenAI ----------
    def call_ai(prompt):
        try:
            client_local = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client_local.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Eres un experto formulador de alimentos y costos."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1800,
                temperature=0.35,
            )

            st.session_state.ai_response = response.choices[0].message.content

        except Exception as e:
            st.error(f"Error al llamar a la API de OpenAI:\n\n{e}")

    if st.button("Generar fórmula con IA"):
        with st.spinner("Generando formulación con IA..."):
            call_ai(prompt_input)

    # Mostrar resultados si existen
    if st.session_state.ai_response:
        st.markdown("### Resultados generados por la IA")
        st.write(st.session_state.ai_response)

    st.button("Volver al inicio", on_click=lambda: st.session_state.update({"paso": 1, "ai_response": None}))
