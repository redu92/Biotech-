import streamlit as st
import json
import pandas as pd
import openai
import streamlit as st

st.write("VERSIÓN OPENAI INSTALADA:", openai.__version__)

# -------------------------------
# CONFIG Y ESTADO INICIAL
# -------------------------------
st.set_page_config(page_title="BiotechSuperfood IA", page_icon="🌿", layout="centered")

# API KEY desde Secrets (Streamlit Cloud)
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", "")
openai.api_key = OPENAI_API_KEY

# Inicializar session_state
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
if "protein_pct" not in st.session_state:
    st.session_state.protein_pct = 0
if "iron_pct" not in st.session_state:
    st.session_state.iron_pct = 0
if "prompt_custom" not in st.session_state:
    st.session_state.prompt_custom = ""
if "ai_result_text" not in st.session_state:
    st.session_state.ai_result_text = ""
if "ai_result_json" not in st.session_state:
    st.session_state.ai_result_json = None

# -------------------------------
# FUNCIONES AUXILIARES
# -------------------------------
def reset_all():
    st.session_state.paso = 1
    st.session_state.usuario = None
    st.session_state.pais = ""
    st.session_state.categoria = ""
    st.session_state.ingredientes = []
    st.session_state.organolepticos = []
    st.session_state.protein_pct = 0
    st.session_state.iron_pct = 0
    st.session_state.prompt_custom = ""
    st.session_state.ai_result_text = ""
    st.session_state.ai_result_json = None

def build_default_prompt():
    # arma prompt con todos los valores seleccionados
    ingredientes = st.session_state.ingredientes or []
    organo = st.session_state.organolepticos or []
    prompt = (
        "Genera una formulación en porcentajes (suma 100%) para un producto tipo "
        f"'{st.session_state.categoria}' destinado a {st.session_state.pais}.\n\n"
        "Incluye lo siguiente (usando los valores proporcionados):\n"
        f"- Ingredientes seleccionados: {', '.join(ingredientes) if ingredientes else 'Ninguno'}.\n"
        f"- Parámetros organolépticos: {', '.join(organo) if organo else 'Ninguno'}.\n"
        f"- Porcentaje objetivo de proteína: {st.session_state.protein_pct}% (usar este valor como guía en la composición total).\n"
        f"- Porcentaje objetivo de hierro (mineral): {st.session_state.iron_pct}% (indicar cómo se logra este % con los ingredientes y/o suplementación).\n\n"
        "Además, CONSIDERA lo siguiente según el país seleccionado (Perú, Colombia o Mexico):\n"
        "- Ajusta la formulación tomando en cuenta costos promedio de insumos y disponibilidad local.\n"
        "- Indica estimación de costo total del lote (moneda local) y desglose por ingrediente aproximado.\n"
        "- Proporciona una tabla nutricional estimada por 100 g para: Valor energético (kcal), Grasas totales (g), Grasas saturadas (g), Grasas trans (g), Sodio (mg), Carbohidratos totales (g), Azúcares (g), Proteínas (g).\n\n"
        "**Formato de salida (OBLIGATORIO):** responde únicamente en JSON con esta estructura EXACTA:\n"
        "{\n"
        '  "formula": [ {"ingredient":"nombre","percent":X}, ... ],\n'
        '  "nutrition_per_100g": {"kcal": X, "fat_g": X, "sat_fat_g": X, "trans_fat_g": X, "sodium_mg": X, "carb_g": X, "sugar_g": X, "protein_g": X},\n'
        '  "cost_total": {"amount": X, "currency": "S/"|"COP"|"MXN"},\n'
        '  "cost_breakdown": [ {"ingredient":"nombre","amount":X}, ... ],\n'
        '  "notes": "breve texto explicativo"\n'
        "}\n\n"
        "Si no puedes estimar algo con precisión, proporciona una mejor estimación razonada en 'notes', pero RESPONDE en JSON válido."
    )
    return prompt

def call_openai_chat(prompt_text):
    if not OPENAI_API_KEY:
        return False, "OpenAI API key no configurada en Secrets."
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # cambia por el modelo que tengas disponible si hace falta
            messages=[
                {"role": "system", "content": "Eres un experto formulador de alimentos y nutrición. Responde en JSON cuando se solicite."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=800,
            temperature=0.6,
        )
        text = resp.choices[0].message.content.strip()
        return True, text
    except Exception as e:
        return False, f"Error llamando a OpenAI: {e}"

# -------------------------------
# UX: HEADER / LOGIN
# -------------------------------
st.title("🌿 BiotechSuperfood IA — Demo")
if st.session_state.usuario is None:
    st.subheader("¡Bienvenido! Ingresa tus credenciales para continuar")
    user = st.text_input("Usuario", key="input_user")
    pwd = st.text_input("Contraseña", type="password", key="input_pwd")
    if st.button("Ingresar"):
        if user == "admin" and pwd == "1234":
            st.session_state.usuario = user
            st.success("Inicio de sesión exitoso")
            st.experimental_rerun()
        else:
            st.error("Usuario o contraseña incorrectos")
    st.stop()

# -------------------------------
# PASO 1: Selección país
# -------------------------------
st.write(f"Usuario: **{st.session_state.usuario}**")
st.header("Paso 1 — Selección de país")
st.session_state.pais = st.selectbox("Seleccione un país", ["", "Perú", "Colombia", "Mexico"], key="sel_pais")
cols = st.columns(3)
if cols[0].button("Atrás", disabled=True):
    pass
if cols[2].button("Siguiente"):
    if st.session_state.pais:
        st.session_state.paso = 2
        st.experimental_rerun()
    else:
        st.error("Selecciona un país antes de continuar.")

# -------------------------------
# PASO 2: Categoría y % proteína
# -------------------------------
if st.session_state.paso >= 2:
    st.header("Paso 2 — Categoría del producto y % proteína")
    categorias = ["", "Mezcla en polvo", "Bebidas", "Snacks", "Suplementos nutricionales", "Productos lacteos", "Productos congelados"]
    st.session_state.categoria = st.selectbox("Selecciona una categoría (solo 1):", categorias, key="cat_step2")
    st.write("**Indica el porcentaje de proteína objetivo (0–90%)**")
    st.session_state.protein_pct = st.number_input("Porcentaje de proteína (%)", min_value=0, max_value=90, value=int(st.session_state.protein_pct or 0), step=1, key="protein_pct")

    cols = st.columns(3)
    if cols[0].button("Atrás"):
        st.session_state.paso = 1
        st.experimental_rerun()
    if cols[2].button("Siguiente"):
        if not st.session_state.categoria:
            st.error("Selecciona una categoría antes de continuar.")
        else:
            st.session_state.paso = 3
            st.experimental_rerun()

# -------------------------------
# PASO 3: Ingredientes y % hierro (en micronutrientes)
# -------------------------------
if st.session_state.paso >= 3:
    st.header("Paso 3 — Selección de ingredientes (puede seleccionar múltiples)")
    st.subheader("Macronutrientes — Proteínas")
    prot_options = ["Aislado de arveja", "Aislado de suero de leche", "Proteína de arroz"]
    for p in prot_options:
        key = f"prot_{p}"
        checked = st.checkbox(p, key=key, value=(p in st.session_state.ingredientes))
        if checked and p not in st.session_state.ingredientes:
            st.session_state.ingredientes.append(p)
        if not checked and p in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(p)

    st.subheader("Macronutrientes — Carbohidratos")
    carb_options = ["Maca", "Quinua", "Cañihua", "Tarwi", "Acelga", "Chia", "Linaza"]
    for c in carb_options:
        key = f"carb_{c}"
        checked = st.checkbox(c, key=key, value=(c in st.session_state.ingredientes))
        if checked and c not in st.session_state.ingredientes:
            st.session_state.ingredientes.append(c)
        if not checked and c in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(c)

    st.subheader("Macronutrientes — Grasas")
    fat_options = ["Aceite de coco", "Aceite de girasol", "Sachi inchi", "Linaza", "Chia", "Aguacate", "Oliva", "Cánamo"]
    for f in fat_options:
        key = f"fat_{f}"
        checked = st.checkbox(f, key=key, value=(f in st.session_state.ingredientes))
        if checked and f not in st.session_state.ingredientes:
            st.session_state.ingredientes.append(f)
        if not checked and f in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(f)

    st.subheader("Micronutrientes y probióticos")
    st.write("**Vitaminas**")
    vit_options = ["Vitamina A", "Vitamina B1", "Vitamina B2", "Vitamina B3"]
    for v in vit_options:
        key = f"vit_{v}"
        checked = st.checkbox(v, key=key, value=(v in st.session_state.ingredientes))
        if checked and v not in st.session_state.ingredientes:
            st.session_state.ingredientes.append(v)
        if not checked and v in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(v)

    st.write("**Minerales**")
    min_options = ["Calcio", "Hierro", "Magnesio", "Fósforo", "Potasio", "Sodio", "Zinc", "Yodo", "Selenio", "Cobre"]
    for m in min_options:
        key = f"min_{m}"
        checked = st.checkbox(m, key=key, value=(m in st.session_state.ingredientes))
        if checked and m not in st.session_state.ingredientes:
            st.session_state.ingredientes.append(m)
        if not checked and m in st.session_state.ingredientes:
            st.session_state.ingredientes.remove(m)

    st.write("**Indica el porcentaje de Hierro que deseas (0–90%) — solo si seleccionaste 'Hierro'**")
    if "Hierro" in st.session_state.ingredientes:
        st.session_state.iron_pct = st.number_input("Porcentaje de Hierro (%)", min_value=0, max_value=90, value=int(st.session_state.iron_pct or 0), step=1, key="iron_pct")
    else:
        st.info("Selecciona 'Hierro' en Minerales para poder fijar un porcentaje objetivo de hierro.")

    cols = st.columns(3)
    if cols[0].button("Atrás"):
        st.session_state.paso = 2
        st.experimental_rerun()
    if cols[2].button("Siguiente"):
        # Validaciones opcionales: si escogió hierro, exigir un porcentaje >0?
        if "Hierro" in st.session_state.ingredientes and st.session_state.iron_pct == 0:
            st.warning("Seleccionaste Hierro pero dejaste 0%. Si quieres aporte de hierro, aumenta el porcentaje o quita 'Hierro' de la lista.")
        st.session_state.paso = 4
        st.experimental_rerun()

# -------------------------------
# PASO 4: Parámetros organolépticos y prompt por defecto
# -------------------------------
if st.session_state.paso >= 4:
    st.header("Paso 4 — Parámetros organolépticos")
    # Organolépticos
    flavor_opts = ["Vainilla", "Cacao", "Frutos deshidratados", "Especias", "Menta", "Cítricos", "Café"]
    sweet_opts = ["Eritritol (E968)", "Stevia (E960)", "Sucralosa"]
    stab_opts = ["Goma Xantana", "Goma Guar", "Pectina", "Goma de tara"]

    for s in flavor_opts:
        key = f"sab_{s}"
        checked = st.checkbox(s, key=key, value=(s in st.session_state.organolepticos))
        if checked and s not in st.session_state.organolepticos:
            st.session_state.organolepticos.append(s)
        if not checked and s in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(s)

    for e in sweet_opts:
        key = f"end_{e}"
        checked = st.checkbox(e, key=key, value=(e in st.session_state.organolepticos))
        if checked and e not in st.session_state.organolepticos:
            st.session_state.organolepticos.append(e)
        if not checked and e in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(e)

    for es in stab_opts:
        key = f"est_{es}"
        checked = st.checkbox(es, key=key, value=(es in st.session_state.organolepticos))
        if checked and es not in st.session_state.organolepticos:
            st.session_state.organolepticos.append(es)
        if not checked and es in st.session_state.organolepticos:
            st.session_state.organolepticos.remove(es)

    st.write("### Prompt que se enviará a ChatGPT (puedes editarlo)")
    # si hay prompt personalizado en sesión, mostrarlo; si no, construir default
    if not st.session_state.prompt_custom:
        st.session_state.prompt_custom = build_default_prompt()
    prompt_val = st.text_area("Prompt (editable)", value=st.session_state.prompt_custom, height=260, key="prompt_area")
    st.session_state.prompt_custom = prompt_val

    cols = st.columns(3)
    if cols[0].button("Atrás"):
        st.session_state.paso = 3
        st.experimental_rerun()
    if cols[2].button("Enviar a ChatGPT (generar formulación)"):
        # Llamada real a OpenAI
        with st.spinner("Enviando prompt a OpenAI y generando formulación..."):
            ok, resp = call_openai_chat(st.session_state.prompt_custom)
            if not ok:
                st.error(resp)
                st.session_state.ai_result_text = resp
                st.session_state.ai_result_json = None
            else:
                st.session_state.ai_result_text = resp
                # intentar parsear JSON
                parsed = None
                try:
                    # a veces la IA encapsula JSON con texto — buscar primer "{" y último "}"
                    first = resp.find("{")
                    last = resp.rfind("}")
                    if first != -1 and last != -1:
                        json_text = resp[first:last+1]
                        parsed = json.loads(json_text)
                    else:
                        parsed = json.loads(resp)
                except Exception:
                    parsed = None
                st.session_state.ai_result_json = parsed
            st.session_state.paso = 5
            st.experimental_rerun()

# -------------------------------
# PASO 5: Mostrar resultado IA, tabla nutricional y costos
# -------------------------------
if st.session_state.paso >= 5:
    st.header("Paso 5 — Resultado de la integración con IA")
    if not st.session_state.ai_result_text:
        st.info("Aún no has generado una formulación con la IA. Regresa al Paso 4 y presiona 'Enviar a ChatGPT'.")
    else:
        st.subheader("Respuesta cruda de ChatGPT")
        st.code(st.session_state.ai_result_text, language="json")

        if st.session_state.ai_result_json:
            data = st.session_state.ai_result_json

            # Mostrar fórmula detallada
            if "formula" in data and isinstance(data["formula"], list):
                st.subheader("Fórmula propuesta (ingrediente — %)")
                df_formula = pd.DataFrame(data["formula"])
                st.table(df_formula)

            # Mostrar tabla nutricional por 100g y por porcion 3.5g
            if "nutrition_per_100g" in data and isinstance(data["nutrition_per_100g"], dict):
                nut = data["nutrition_per_100g"]
                df_nut = pd.DataFrame({
                    "Nutriente": ["Valor energético (kcal)", "Grasas totales (g)", "Grasas saturadas (g)",
                                  "Grasas trans (g)", "Sodio (mg)", "Carbohidratos totales (g)", "Azúcares (g)", "Proteínas (g)"],
                    "Por 100 g": [
                        nut.get("kcal", None),
                        nut.get("fat_g", None),
                        nut.get("sat_fat_g", None),
                        nut.get("trans_fat_g", None),
                        nut.get("sodium_mg", None),
                        nut.get("carb_g", None),
                        nut.get("sugar_g", None),
                        nut.get("protein_g", None),
                    ]
                })
                # Calcular por porción 3.5 g
                df_nut["Por porción (3.5 g)"] = (pd.to_numeric(df_nut["Por 100 g"], errors="coerce") * 0.035).round(2)
                st.subheader("Tabla nutricional estimada")
                st.table(df_nut.fillna("N/A"))

            # Mostrar costos
            if "cost_total" in data:
                ct = data["cost_total"]
                st.subheader("Costo estimado")
                amount = ct.get("amount", "N/A")
                currency = ct.get("currency", "")
                st.metric("Costo total estimado", f"{amount} {currency}")

            if "cost_breakdown" in data and isinstance(data["cost_breakdown"], list):
                st.subheader("Desglose de costos (aprox.)")
                df_cost = pd.DataFrame(data["cost_breakdown"])
                st.table(df_cost)
            if "notes" in data:
                st.info(f"Notas de la IA: {data['notes']}")

        else:
            st.warning("La IA no devolvió JSON parseable. A continuación se muestra la respuesta cruda. Puedes editar el prompt para forzar un JSON válido.")
            st.write(st.session_state.ai_result_text)

    cols = st.columns(3)
    if cols[0].button("← Atrás"):
        st.session_state.paso = 4
        st.experimental_rerun()
    if cols[2].button("Reiniciar demo"):
        reset_all()
        st.experimental_rerun()
