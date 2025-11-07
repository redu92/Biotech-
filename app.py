import streamlit as st

# -------------------------------
# CONFIGURACIÓN Y ESTADO INICIAL
# -------------------------------
st.set_page_config(page_title="BiotechSuperfood IA", page_icon="🌿", layout="centered")

# Inicializar variables de sesión si no existen
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

# -------------------------------
# FUNCIONES UTILES
# -------------------------------
def reset_pasos():
    st.session_state.paso = 1
    st.session_state.pais = ""
    st.session_state.categoria = ""
    st.session_state.ingredientes = []
    st.session_state.organolepticos = []
    st.session_state.usuario = None

# -------------------------------
# CSS y recursos visuales
# -------------------------------
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #E9F5FF 0%, #FFFFFF 100%);
    }
    h1, h2, h3 { color: #0056B3 !important; font-weight: 700 !important; }
    div.stButton > button {
        background-color: #0078D7;
        color: white;
        border-radius: 10px;
        height: 42px;
        font-weight: 700;
        border: none;
    }
    div.stButton > button:hover { background-color: #0056B3; color: #E0EFFF; }
    .stTextInput input { border: 1px solid #0078D7; border-radius: 8px; }
    [data-testid="stMetricValue"] { color: #0078D7; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

IMAGEN_LOGO = "https://cdn-icons-png.flaticon.com/512/4149/4149723.png"
IMAGEN_IA = "https://cdn-icons-png.flaticon.com/512/4712/4712105.png"
IMAGEN_FORMULA = "https://cdn-icons-png.flaticon.com/512/1048/1048947.png"

# -------------------------------
# FLUJO: LOGIN
# -------------------------------
if st.session_state.usuario is None:
    st.image(IMAGEN_LOGO, width=110)
    st.title("🌿 ¡Bienvenido a BiotechSuperfood IA!")
    st.subheader("Optimiza tus fórmulas con Inteligencia Artificial")
    st.write("Ingrese sus credenciales para continuar:")

    usuario = st.text_input("👤 Usuario", key="input_usuario")
    contraseña = st.text_input("🔒 Contraseña", type="password", key="input_contra")

    if st.button("Ingresar"):
        if usuario == "admin" and contraseña == "1234":
            st.session_state.usuario = usuario
            st.success("Inicio de sesión exitoso ✅")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
# -------------------------------
# PASO 1: Selección de país
# -------------------------------
elif st.session_state.paso == 1:
    st.image(IMAGEN_LOGO, width=80)
    st.header("🌎 Paso 1: Selección de país")
    st.session_state.pais = st.selectbox("Seleccione un país", ["", "Perú", "Colombia", "México"], key="sel_pais")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", disabled=True)
    with col2:
        if st.button("Siguiente"):
            if st.session_state.pais:
                st.session_state.paso = 2
                st.rerun()
            else:
                st.error("Por favor selecciona un país para continuar.")
# -------------------------------
# PASO 2: Selección de categoría
# -------------------------------
elif st.session_state.paso == 2:
    st.image(IMAGEN_LOGO, width=80)
    st.header("🥤 Paso 2: Categoría del producto")
    categorias = [
        "Mezcla en polvo",
        "Bebidas",
        "Snacks",
        "Suplementos nutricionales",
        "Productos lácteos",
        "Productos congelados",
    ]
    st.session_state.categoria = st.radio("Seleccione una categoría:", categorias, key="radio_categoria")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 1
            st.rerun()
    with col2:
        if st.button("Siguiente"):
            if st.session_state.categoria:
                st.session_state.paso = 3
                st.rerun()
            else:
                st.error("Por favor selecciona una categoría.")
# -------------------------------
# PASO 3: Selección de ingredientes
# -------------------------------
elif st.session_state.paso == 3:
    st.image(IMAGEN_FORMULA, width=100)
    st.header("🌾 Paso 3: Selección de ingredientes (puede seleccionar múltiples)")

    def checkboxes_opciones(titulo, opciones, prefijo):
        st.markdown(f"**{titulo}**")
        for op in opciones:
            key = f"{prefijo}_{op}"
            checked = st.checkbox(op, key=key)
            if checked and op not in st.session_state.ingredientes:
                st.session_state.ingredientes.append(op)
            elif not checked and op in st.session_state.ingredientes:
                st.session_state.ingredientes.remove(op)

    st.subheader("Macronutrientes — Proteínas")
    checkboxes_opciones("", ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"], "prot")
    st.subheader("Macronutrientes — Carbohidratos")
    checkboxes_opciones("", ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"], "carb")
    st.subheader("Macronutrientes — Grasas")
    checkboxes_opciones("", ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cáñamo"], "gras")

    st.subheader("Micronutrientes y probióticos — Vitaminas")
    checkboxes_opciones("", ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"], "vit")
    st.subheader("Micronutrientes y probióticos — Minerales")
    checkboxes_opciones("", ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"], "min")

    st.write("**Ingredientes seleccionados:**", ", ".join(st.session_state.ingredientes) if st.session_state.ingredientes else "— Ninguno —")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 2
            st.rerun()
    with col2:
        if st.button("Siguiente"):
            if st.session_state.ingredientes:
                st.session_state.paso = 4
                st.rerun()
            else:
                st.error("Selecciona al menos un ingrediente para continuar.")
# -------------------------------
# PASO 4: Parámetros organolépticos
# -------------------------------
elif st.session_state.paso == 4:
    st.image(IMAGEN_IA, width=100)
    st.header("🍫 Paso 4: Parámetros organolépticos (selección múltiple)")

    def checkboxes_organolepticos(titulo, opciones, prefijo):
        st.markdown(f"**{titulo}**")
        for op in opciones:
            key = f"{prefijo}_{op}"
            checked = st.checkbox(op, key=key)
            if checked and op not in st.session_state.organolepticos:
                st.session_state.organolepticos.append(op)
            elif not checked and op in st.session_state.organolepticos:
                st.session_state.organolepticos.remove(op)

    checkboxes_organolepticos("Saborizantes", ["Vainilla", "Cacao", "Frutos deshidratados", "Especias", "Menta", "Cítricos", "Café"], "sab")
    checkboxes_organolepticos("Endulcorantes", ["Eritritol (E968)", "Stevia (E960)", "Sucralosa"], "end")
    checkboxes_organolepticos("Estabilizantes", ["Goma Xantana", "Goma Guar", "Pectina", "Goma de Tara"], "est")

    st.write("**Parámetros seleccionados:**", ", ".join(st.session_state.organolepticos) if st.session_state.organolepticos else "— Ninguno —")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 3
            st.rerun()
    with col2:
        if st.button("Siguiente"):
            st.session_state.paso = 5
            st.rerun()
# -------------------------------
# PASO 5: Integración con IA (prompt)
# -------------------------------
elif st.session_state.paso == 5:
    st.image(IMAGEN_IA, width=120)
    st.header("🤖 Paso 5: Integración con IA")
    st.write("Ingrese un prompt personalizado o deje vacío para generar automáticamente una fórmula con las selecciones realizadas.")

    prompt = st.text_area("Prompt para ChatGPT (opcional)", placeholder="Ejemplo: Genera una fórmula balanceada con los ingredientes seleccionados...")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 4
            st.rerun()
    with col2:
        if st.button("Generar fórmula integrada con IA"):
            # Aquí sólo simulamos la llamada; si tienes OpenAI configurado se puede llamar real.
            st.session_state.paso = 6
            # (en una versión con OpenAI, aquí harías la llamada y guardarías la respuesta)
            st.rerun()
# -------------------------------
# PASO 6: Resultados finales
# -------------------------------
elif st.session_state.paso == 6:
    st.image(IMAGEN_FORMULA, width=120)
    st.header("📊 Resultados de la fórmula generada")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Costo estimado", "S/ 8.00")
    col2.metric("Peso total", "100 g")
    col3.metric("Porciones", "28")
    col4.metric("Tamaño por porción", "3.5 g")
    
     st.subheader("Fórmula (simulada)")
    # Si integras OpenAI, mostrarás la respuesta real aquí. Por ahora mostramos un texto placeholder.
    st.info("Fórmula generada con los ingredientes seleccionados (simulada). Si configuras OpenAI, aquí aparecerá la respuesta real.")

    st.subheader("Tabla nutricional estimada (por 100 g y porción de 3.5 g)")
    st.table({
        "Nutriente": ["Valor energético (kcal)", "Grasas totales (g)", "Grasas saturadas (g)", "Grasas trans (g)", "Sodio (mg)", "Carbohidratos totales (g)", "Azúcares (g)", "Proteína (g)"],
        "Por 100 g": [400, 12, 3, 0, 50, 45, 20, 25],
        "Por porción (3.5 g)": [14, 0.4, 0.1, 0, 1.8, 1.6, 0.7, 0.9],
    })

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔁 Volver al inicio"):
            reset_pasos()
            st.rerun()
    with col2:
        if st.button("Cerrar sesión"):
            reset_pasos()
            st.session_state.usuario = None
            st.rerun()




