import streamlit as st
from groq import Groq
import os

st.title("Modelos disponibles en Groq")

# Cargar API Key desde variable de entorno
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("No existe GROQ_API_KEY en tus variables de entorno.")
    st.stop()

try:
    client = Groq(api_key=api_key)
    st.info("Consultando modelos disponibles...")

    models = client.models.list()

    st.success("Modelos encontrados:")

    for m in models.data:
        st.write(f"🔹 **{m.id}**")

except Exception as e:
    st.error(f"Error llamando a Groq: {e}")
