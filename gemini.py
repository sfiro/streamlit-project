import streamlit as st
import google.generativeai as genai
import os


# --- Configuración Segura de la API de Gemini ---
# Usar Streamlit Secrets o Variables de Entorno para la clave de API
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]  # Para despliegue en Streamlit Cloud
except AttributeError:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Para desarrollo local

if not GOOGLE_API_KEY:
    st.error("🚨 La clave de API de Google no está configurada.")
    st.stop()

# Configura la API key en la librería de Google Generative AI
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error(f"Error al configurar la API de Gemini: {e}")
    st.stop()

def chat():
    # --- Interfaz de Usuario con Streamlit ---
    st.title("🤖 Chat con Gemini")
    st.write("Interactúa con el sistema de chat de Google Generative AI (Gemini).")

    # Configurar la API

    client = genai.Client(api_key="YOUR_API_KEY")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Explain how AI works in a few words",
    )

    print(response.text)

