import streamlit as st

# -------------------------------------------------
# Inicialización del estado de sesión
# -------------------------------------------------
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


# -------------------------------------------------
# Función para reiniciar pasos
# -------------------------------------------------
def reset_pasos():
    st.session_state.paso = 1
    st.session_state.pais = ""
    st.session_state.categoria = ""
    st.session_state.ingredientes = []
    st.session_state.organolepticos = []


# -------------------------------------------------
# Paso 0: Inicio de sesión
# -------------------------------------------------
if st.session_state.usuario is None:
    st.title("¡Bienvenido a BiotechSuperfood IA!")
    st.write("Ingrese sus credenciales para continuar:")

    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if usuario == "admin" and contraseña == "1234":
            st.session_state.usuario = usuario
            st.success("Inicio de sesión exitoso ✅")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

# -------------------------------------------------
# Paso 1: Selección de país
# -------------------------------------------------
elif st.session_state.paso == 1:
    st.header("Paso 1: Selección de país")
    st.session_state.pais = st.selectbox("Seleccione un país", ["", "Perú", "Colombia", "México"])

    col1, col2 = st.columns(2)
    with col1:
        st.button("Atrás", disabled=True)
    with col2:
        if st.button("Siguiente") and st.session_state.pais != "":
            st.session_state.paso = 2
            st.rerun()

# -------------------------------------------------
# Paso 2: Selección de categoría del producto
# -------------------------------------------------
elif st.session_state.paso == 2:
    st.header("Paso 2: Categoría del producto")
    categorias = [
        "Mezcla en polvo",
        "Bebidas",
        "Snacks",
        "Suplementos nutricionales",
        "Productos lácteos",
        "Productos congelados",
    ]
    st.session_state.categoria = st.radio("Seleccione una categoría", categorias, index=None)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 1
            st.rerun()
    with col2:
        if st.button("Siguiente") and st.session_state.categoria:
            st.session_state.paso = 3
            st.rerun()

# -------------------------------------------------
# Paso 3: Selección de ingredientes
# -------------------------------------------------
elif st.session_state.paso == 3:
    st.header("Paso 3: Selección de ingredientes")

    st.subheader("Macronutrientes")
    st.markdown("**Proteínas**")
    proteinas = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]
    for p in proteinas:
        if st.checkbox(p, key=f"prote_{p}", value=(p in st.session_state.ingredientes)):
            if p not in st.session_state.ingredientes:
                st.session_state.ingredientes.append(p)
        elif p in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(p)

    st.markdown("**Carbohidratos**")
    carbos = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"]
    for c in carbos:
        if st.checkbox(c, key=f"carb_{c}", value=(c in st.session_state.ingredientes)):
            if c not in st.session_state.ingredientes:
                st.session_state.ingredientes.append(c)
        elif c in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(c)

    st.markdown("**Grasas**")
    grasas = ["Aceite de coco", "Aceite de girasol", "Sacha Inchi", "Linaza", "Chía", "Aguacate", "Oliva", "Cáñamo"]
    for g in grasas:
        if st.checkbox(g, key=f"gras_{g}", value=(g in st.session_state.ingredientes)):
            if g not in st.session_state.ingredientes:
                st.session_state.ingredientes.append(g)
        elif g in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(g)

    st.subheader("Micronutrientes y probióticos")
    st.markdown("**Vitaminas**")
    vitaminas = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    for v in vitaminas:
        if st.checkbox(v, key=f"vit_{v}", value=(v in st.session_state.ingredientes)):
            if v not in st.session_state.ingredientes:
                st.session_state.ingredientes.append(v)
        elif v in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(v)

    st.markdown("**Minerales**")
    minerales = [
        "Calcio",
        "Hierro",
        "Magnesio",
        "Fósforo",
        "Potasio",
        "Sodio",
        "Zinc",
        "Yodo",
        "Selenio",
        "Cobre",
    ]
    for m in minerales:
        if st.checkbox(m, key=f"min_{m}", value=(m in st.session_state.ingredientes)):
            if m not in st.session_state.ingredientes:
                st.session_state.ingredientes.append(m)
        elif m in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(m)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 2
            st.rerun()
    with col2:
        if st.button("Siguiente"):
            st.session_state.paso = 4
            st.rerun()

# -------------------------------------------------
# Paso 4: Selección de parámetros organolépticos
# -------------------------------------------------
elif st.session_state.paso == 4:
    st.header("Paso 4: Parámetros organolépticos")

    st.subheader("Saborizantes")
    saborizantes = ["Vainilla", "Cacao", "Frutos deshidratados", "Especias", "Menta", "Cítricos", "Café"]
    for s in saborizantes:
        if st.checkbox(s, key=f"sab_{s}", value=(s in st.session_state.organolepticos)):
            if s not in st.session_state.organolepticos:
                st.session_state.organolepticos.append(s)
        elif s in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(s)

    st.subheader("Endulzantes")
    endulzantes = ["Eritritol (E968)", "Stevia (E960)", "Sucralosa"]
    for e in endulzantes:
        if st.checkbox(e, key=f"end_{e}", value=(e in st.session_state.organolepticos)):
            if e not in st.session_state.organolepticos:
                st.session_state.organolepticos.append(e)
        elif e in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(e)

    st.subheader("Estabilizantes")
    estabilizantes = ["Goma Xantana", "Goma Guar", "Pectina", "Goma de Tara"]
    for es in estabilizantes:
        if st.checkbox(es, key=f"est_{es}", value=(es in st.session_state.organolepticos)):
            if es not in st.session_state.organolepticos:
                st.session_state.organolepticos.append(es)
        elif es in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(es)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atrás"):
            st.session_state.paso = 3
            st.rerun()
    with col2:
        if st.button("Siguiente"):
            st.session_state.paso = 5
            st.rerun()

# -------------------------------------------------
# Paso 5: Integración con IA
# -------------------------------------------------
elif st.session_state.paso == 5:
    st.header("Integración con IA")
    st.write("Puedes escribir un prompt personalizado o generar una fórmula automáticamente con los ingredientes seleccionados.")

    prompt = st.text_area("Prompt para ChatGPT", placeholder="Ejemplo: Genera una fórmula balanceada con los ingredientes seleccionados...")

    if st.button("Generar fórmula integrada con IA"):
        with st.spinner("🔄 Generando Fórmula..."):
            st.session_state.paso = 6
            st.rerun()

# -------------------------------------------------
# Paso 6: Resultados
# -------------------------------------------------
elif st.session_state.paso == 6:
    st.header("Resultados de la fórmula generada")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Costo estimado", "S/ 8.00")
    col2.metric("Peso total", "100 g")
    col3.metric("Porciones", "28")
    col4.metric("Tamaño por porción", "3.5 g")

    st.subheader("Tabla nutricional estimada (por 100 g y porción de 3.5 g)")
    st.table({
        "Nutriente": [
            "Valor energético",
            "Grasas totales",
            "Grasas saturadas",
            "Grasas trans",
            "Sodio",
            "Carbohidratos totales",
            "Azúcares",
            "Proteína"
        ],
        "Por 100 g": [400, 12, 3, 0, 50, 45, 20, 25],
        "Por porción (3.5 g)": [14, 0.4, 0.1, 0, 1.8, 1.6, 0.7, 0.9],
    })

    if st.button("🔁 Volver al inicio"):
        reset_pasos()
        st.session_state.usuario = None
        st.rerun()

