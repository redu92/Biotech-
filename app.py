import streamlit as st
import openai
import sqlite3
from datetime import datetime
import pandas as pd

# ===========================
# CONFIG
# ===========================
st.set_page_config(page_title="BiotechSuperfood IA - Demo", layout="wide", page_icon="🧪")

# Pon tu API key aquí o mejor usar variable de entorno
OPENAI_API_KEY = "TU_API_KEY_AQUI"
openai.api_key = OPENAI_API_KEY

# ===========================
# BASE DE DATOS (SQLite)
# ===========================
conn = sqlite3.connect("biotech_demo.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS formulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT,
    fecha TEXT,
    pais TEXT,
    categoria TEXT,
    ingredientes TEXT,
    organolepticos TEXT,
    prompt TEXT,
    resultado_ai TEXT
)
''')
conn.commit()

# ===========================
# UTILIDADES
# ===========================
def guardar_formula(usuario, pais, categoria, ingredientes, organolepticos, prompt, resultado):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute(
        "INSERT INTO formulas (usuario, fecha, pais, categoria, ingredientes, organolepticos, prompt, resultado_ai) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (usuario, fecha, pais, categoria, ", ".join(ingredientes), ", ".join(organolepticos), prompt, resultado)
    )
    conn.commit()

def llamar_chatgpt(prompt_text):
    """Llama a la API de OpenAI (ChatCompletion) y devuelve texto. Ajusta el modelo según tu acceso."""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # ajusta si necesario
            messages=[
                {"role": "system", "content": "Eres un experto formulador de alimentos nutricionales. Responde con una fórmula clara y breve."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=600,
            temperature=0.7,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error al conectar con la API de OpenAI: {e}"

# ===========================
# INICIALIZAR SESION
# ===========================
if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "step" not in st.session_state:
    st.session_state.step = 1
# valores guardados entre pasos
if "pais" not in st.session_state:
    st.session_state.pais = None
if "categoria" not in st.session_state:
    st.session_state.categoria = None
if "ingredientes" not in st.session_state:
    st.session_state.ingredientes = []
if "organolepticos" not in st.session_state:
    st.session_state.organolepticos = []
if "prompt_custom" not in st.session_state:
    st.session_state.prompt_custom = ""
if "resultado_ai" not in st.session_state:
    st.session_state.resultado_ai = ""

# ===========================
# HEADER / LOGIN
# ===========================
st.markdown("# ¡Bienvenido a BiotechSuperfood IA!")
st.write("Ingrese sus credenciales para continuar")

col1, col2 = st.columns([2, 1])
with col1:
    usuario_input = st.text_input("Usuario")
with col2:
    pwd_input = st.text_input("Contraseña", type="password")

if not st.session_state.logueado:
    if st.button("Ingresar"):
        if usuario_input == "admin" and pwd_input == "1234":
            st.session_state.logueado = True
            st.session_state.usuario = usuario_input
            st.success(f"Bienvenido, {usuario_input} 👋")
            st.session_state.step = 1
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")
    st.stop()  # no mostrar el resto si no está logueado

# Si está logueado:
st.sidebar.success(f"Usuario: {st.session_state.usuario}")
if st.sidebar.button("Cerrar sesión"):
    st.session_state.logueado = False
    st.session_state.usuario = ""
    st.session_state.step = 1
    st.rerun()

# ===========================
# NAVIGATION Y FUNCIONES DE STEP
# ===========================
def go_next():
    st.session_state.step += 1
    st.rerun()

def go_back():
    if st.session_state.step > 1:
        st.session_state.step -= 1
        st.rerun()

# Layout principal por pasos
st.write("---")
st.markdown(f"### Paso {st.session_state.step}")

# ---------------------------
# Paso 1: Selección de país
# ---------------------------
if st.session_state.step == 1:
    st.subheader("Selecciona el país")
    pais = st.selectbox("País", ["Perú", "Colombia", "Mexico"], index=0 if st.session_state.pais is None else ["Perú","Colombia","Mexico"].index(st.session_state.pais))
    st.session_state.pais = pais

    cols = st.columns(3)
    cols[0].button("Atrás", on_click=go_back, disabled=True)  # en paso 1 no se puede ir atrás
    cols[1].write("")  # espacio
    if cols[2].button("Siguiente"):
        go_next()

# ---------------------------
# Paso 2: Selección de categoría (bloques, 1 sola opción)
# ---------------------------
elif st.session_state.step == 2:
    st.subheader("Paso 2 — Selecciona la categoría del producto")
    st.write("Elige una sola categoría (haz clic en el bloque correspondiente).")

    opciones = ["Mezcla en polvo", "Bebidas", "Snacks", "Suplementos nutricionales", "Productos lacteos", "Productos congelados"]

    # Mostrar como bloques en filas de 3 columnas
    cols = st.columns(3)
    for i, opt in enumerate(opciones):
        col = cols[i % 3]
        # si el bloque es la selección actual, lo indicamos
        seleccionado_text = "✅ Seleccionado" if st.session_state.categoria == opt else ""
        if col.button(f"{opt}\n{seleccionado_text}", key=f"cat_{i}"):
            st.session_state.categoria = opt
            st.rerun()


    st.write(f"**Seleccionado:** {st.session_state.categoria if st.session_state.categoria else 'Nada seleccionado todavía'}")
    btns = st.columns(3)
    if btns[0].button("Atrás"):
        go_back()
    if btns[2].button("Siguiente"):
        if not st.session_state.categoria:
            st.error("Debes seleccionar una categoría antes de continuar.")
        else:
            go_next()

# -------------------------------
# PASO 3: Selección de ingredientes
# -------------------------------
if st.session_state.paso >= 3:
    st.header("Paso 3️⃣: Selección de ingredientes")

    st.subheader("Macronutrientes")
    st.write("**Proteínas:**")
    proteinas = st.multiselect(
        "",
        ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"],
        key="proteinas",
    )

    st.write("**Carbohidratos:**")
    carbos = st.multiselect(
        "",
        ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chía", "Linaza"],
        key="carbohidratos",
    )

    st.write("**Grasas:**")
    grasas = st.multiselect(
        "",
        [
            "Aceite de coco",
            "Aceite de girasol",
            "Sacha inchi",
            "Linaza",
            "Chía",
            "Aguacate",
            "Oliva",
            "Cañamo",
        ],
        key="grasas",
    )

    st.subheader("Micronutrientes y probióticos")
    st.write("**Vitaminas:**")
    vitaminas = st.multiselect(
        "",
        ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"],
        key="vitaminas",
    )

    st.write("**Minerales:**")
    minerales = st.multiselect(
        "",
        [
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
        ],
        key="minerales",
    )

    col1, col2 = st.columns(2)
    if col1.button("← Atrás", key="p3_back"):
        st.session_state.paso = 2
        st.rerun()
    if col2.button("Siguiente →", key="p3_next"):
        st.session_state.paso = 4
        st.rerun()


# ---------------------------
# Paso 4: Parametros organolepticos (multiselección)
# ---------------------------
elif st.session_state.step == 4:
    st.subheader("Paso 4 — Selección de Parámetros Organolépticos (perfil de sabor, dulzor y texturas)")

    st.markdown("**Saborizantes**")
    saborizantes = ["Vainilla", "Cacao", "Frutos deshidratados", "Especias", "Menta", "Cítricos", "Café"]
    for s in saborizantes:
        checked = st.checkbox(s, value=(s in st.session_state.organolepticos))
        if checked and s not in st.session_state.organolepticos:
            st.session_state.organolepticos.append(s)
        if not checked and s in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(s)

    st.markdown("**Endulcorantes**")
    endulc = ["Eritritol (E968)", "Stevia (E960)", "Sucralosa"]
    for s in endulc:
        checked = st.checkbox(s, value=(s in st.session_state.organolepticos))
        if checked and s not in st.session_state.organolepticos:
            st.session_state.organolepticos.append(s)
        if not checked and s in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(s)

    st.markdown("**Estabilizantes**")
    estabs = ["Goma Xantana", "Goma Guar", "Pectina", "Goma de tara"]
    for s in estabs:
        checked = st.checkbox(s, value=(s in st.session_state.organolepticos))
        if checked and s not in st.session_state.organolepticos:
            st.session_state.organolepticos.append(s)
        if not checked and s in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(s)

    st.write("**Parámetros seleccionados:**")
    if st.session_state.organolepticos:
        st.write(", ".join(st.session_state.organolepticos))
    else:
        st.info("No hay parámetros seleccionados aún.")

    btns = st.columns(3)
    if btns[0].button("Atrás"):
        go_back()
    if btns[2].button("Siguiente"):
        # No requerimos selección, pero puedes validar si quieres
        go_next()

# ---------------------------
# Paso 5: Integración con IA / Generar fórmula
# ---------------------------
elif st.session_state.step == 5:
    st.subheader("Integración con IA")
    st.write("Escribe un prompt para ChatGPT (si dejas vacío se generará uno automático usando las selecciones realizadas).")

    default_prompt = ""
    if st.session_state.prompt_custom:
        default_prompt = st.session_state.prompt_custom
    else:
        # generar prompt por defecto basado en selecciones
        default_prompt = (
            f"Formula una receta/porcentaje de ingredientes para un producto tipo '{st.session_state.categoria}' "
            f"destinado a {st.session_state.pais}. Usa estos ingredientes: {', '.join(st.session_state.ingredientes)}. "
            f"Incorpora estos parámetros organolépticos: {', '.join(st.session_state.organolepticos)}. "
            "Presenta la fórmula en porcentajes para un total de 100 g y una breve justificación técnica."
        )

    st.session_state.prompt_custom = st.text_area("Prompt para ChatGPT", value=default_prompt, height=200)

    if st.button("Generar fórmula integrada con IA"):
        # Llamada a ChatGPT
        with st.spinner("Generando Formula..."):
            prompt_to_send = st.session_state.prompt_custom
            resultado = llamar_chatgpt(prompt_to_send)
            st.session_state.resultado_ai = resultado
            # guardar en BD
            guardar_formula(
                st.session_state.usuario,
                st.session_state.pais,
                st.session_state.categoria,
                st.session_state.ingredientes,
                st.session_state.organolepticos,
                prompt_to_send,
                resultado
            )
            st.success("Fórmula generada y guardada.")

    # Mostrar resultado (si existe)
    if st.session_state.resultado_ai:
        st.markdown("### Resultado de la IA (Fórmula propuesta)")
        st.info(st.session_state.resultado_ai)

        # Mostrar los 4 rectángulos con valores fijos
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Costo estimado", "S/ 8.00")
        col2.metric("Peso total", "100 g")
        col3.metric("Porciones", "28")
        col4.metric("Tamaño de porción", "3.5 g")

        st.markdown("### Tabla nutricional estimada")
        # Valores ficticios por 100g (puedes ajustar o calcular según ingredientes)
        datos_100g = {
            "Nutriente": [
                "Valor energético (kcal)",
                "Grasas totales (g)",
                "Grasas saturadas (g)",
                "Grasas trans (g)",
                "Sodio (mg)",
                "Carbohidratos totales (g)",
                "Azúcares (g)",
                "Proteínas (g)"
            ],
            "Por 100 g": [420, 12.0, 3.5, 0.0, 250, 48.0, 10.0, 20.0]
        }
        df = pd.DataFrame(datos_100g)
        # calcular por porción 3.5 g (multiplicar por 0.035)
        df["Por porción (3.5 g)"] = (df["Por 100 g"] * 0.035).round(2)
        # Asegurar formato legible
        df_display = df.copy()
        df_display["Por 100 g"] = df_display["Por 100 g"].astype(str)
        df_display["Por porción (3.5 g)"] = df_display["Por porción (3.5 g)"].astype(str)
        st.dataframe(df, use_container_width=True)

    btns = st.columns(3)
    if btns[0].button("Atrás"):
        go_back()
    if btns[2].button("Reiniciar todo"):
        # limpia sesión
        st.session_state.step = 1
        st.session_state.pais = None
        st.session_state.categoria = None
        st.session_state.ingredientes = []
        st.session_state.organolepticos = []
        st.session_state.prompt_custom = ""
        st.session_state.resultado_ai = ""
        st.rerun()


# ===========================
# FOOTER: Ver historial (opcional)
# ===========================
st.write("---")
with st.expander("Ver historial de fórmulas generadas (últimas 20)"):
    df_hist = pd.read_sql_query("SELECT id, usuario, fecha, pais, categoria, ingredientes FROM formulas ORDER BY id DESC LIMIT 20", conn)
    if not df_hist.empty:
        st.table(df_hist)
    else:
        st.info("Aún no hay fórmulas guardadas.")
