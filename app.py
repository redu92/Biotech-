import streamlit as st
from groq import Groq
import os

# -------------------------------
# Inicializar sesión
# -------------------------------
if "paso" not in st.session_state:
    st.session_state.paso = 1

if "prompt_final" not in st.session_state:
    st.session_state.prompt_final = ""

if "resultado_ia" not in st.session_state:
    st.session_state.resultado_ia = ""

# -------------------------------
# Función para llamar Groq
# -------------------------------
def llamar_groq(prompt):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1200
        )

        return response.choices[0].message["content"]

    except Exception as e:
        st.error(f"Error al llamar a Groq: {e}")
        return None


# -------------------------------
# UI
# -------------------------------
st.title("🧪 Generador de Formulaciones con IA (Groq API)")

# Paso 1 -----------------------------------------
if st.session_state.paso == 1:
    st.subheader("📌 Paso 1: Datos del alimento")

    st.session_state.product_name = st.text_input("Nombre del alimento:", "")
    st.session_state.protein_pct = st.number_input("Proteína (%)", 0, 90, 20)
    st.session_state.fat_pct = st.number_input("Grasa (%)", 0, 90, 5)
    st.session_state.fiber_pct = st.number_input("Fibra (%)", 0, 40, 3)
    st.session_state.moisture_pct = st.number_input("Humedad (%)", 0, 80, 10)

    if st.button("Siguiente ➡️"):
        st.session_state.paso = 2

# Paso 2 -----------------------------------------
elif st.session_state.paso == 2:
    st.subheader("📌 Paso 2: Ingredientes disponibles")

    st.session_state.available_ingredients = st.text_area(
        "Lista de ingredientes disponibles (uno por línea):",
        "Harina de maíz\nHarina de soya\nAfrecho de trigo\nAceite vegetal"
    )

    if st.button("Siguiente ➡️"):
        st.session_state.paso = 3

    if st.button("⬅️ Volver"):
        st.session_state.paso = 1

# Paso 3 -----------------------------------------
elif st.session_state.paso == 3:
    st.subheader("📌 Paso 3: Generar prompt")

    # Construcción del prompt
    prompt = f"""
Eres un formulador experto en nutrición animal. Construye una formulación balanceada.

DATOS DEL PRODUCTO:
- Nombre: {st.session_state.product_name}
- Proteína objetivo: {st.session_state.protein_pct} %
- Grasa objetivo: {st.session_state.fat_pct} %
- Fibra máxima: {st.session_state.fiber_pct} %
- Humedad: {st.session_state.moisture_pct} %

INGREDIENTES DISPONIBLES:
{st.session_state.available_ingredients}

Genera:
1. Una formulación completa con porcentajes.
2. Justificación técnica.
3. Advertencias o limitaciones.
    """

    st.session_state.prompt_final = prompt

    st.text_area("Prompt generado:", prompt, height=250)

    if st.button("Generar formulación con IA 🤖"):
        with st.spinner("Llamando a Groq…"):
            result = llamar_groq(prompt)

        if result:
            st.session_state.resultado_ia = result
            st.session_state.paso = 4

    if st.button("⬅️ Volver"):
        st.session_state.paso = 2

# Paso 4 -----------------------------------------
elif st.session_state.paso == 4:
    st.subheader("📌 Resultado de la Formulación con IA")

    if st.session_state.resultado_ia:
        st.success("✅ Formulación generada exitosamente:")
        st.markdown(st.session_state.resultado_ia)
    else:
        st.error("❌ No se obtuvo respuesta de la IA.")

    if st.button("⬅️ Volver al inicio"):
        st.session_state.paso = 1

