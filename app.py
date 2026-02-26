import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64


# CONFIGURACIÓN DE PÁGINA


st.set_page_config(
    page_title="Escúchalo - Lector Accesible",
    page_icon="🎧",
    layout="centered"
)


# ESTILO PERSONALIZADO


st.markdown("""
<style>
.main {
    background-color: #F4F6F9;
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #2C3E50;
}
.stButton>button {
    background-color: #4A90E2;
    color: white;
    border-radius: 8px;
    padding: 0.5em 1em;
}
</style>
""", unsafe_allow_html=True)


# HEADER


st.markdown("## 🎧 Escúchalo")
st.markdown("### Lector Accesible de Texto a Voz")
st.markdown("Convierte cualquier texto en una experiencia auditiva accesible.")

# Imagen (cámbiala por una más minimalista si deseas)
image = Image.open('gato.jpg')
st.image(image, width=300)

st.markdown("---")


# SIDEBAR

with st.sidebar:
    st.header("⚙ Opciones")
    st.markdown("Selecciona el idioma y velocidad de lectura.")


# CREAR CARPETA TEMP


try:
    os.mkdir("temp")
except:
    pass


# ENTRADA DE TEXTO


st.subheader("📥 Escribe o pega tu texto:")

text = st.text_area(
    "Texto a convertir",
    height=200,
    placeholder="Pega aquí tu texto..."
)

# Contador de palabras
if text:
    word_count = len(text.split())
    st.caption(f"Cantidad de palabras: {word_count}")


# SELECCIÓN DE IDIOMA


option_lang = st.selectbox(
    "🌎 Selecciona el idioma",
    ("Español", "English")
)

if option_lang == "Español":
    lg = "es"
else:
    lg = "en"


# OPCIÓN DE LECTURA LENTA


slow_option = st.checkbox("🔎 Lectura lenta (Recomendado para dislexia o baja visión)")


# FUNCIÓN TEXTO A VOZ


def text_to_speech(text, lg, slow_option):
    
    tts = gTTS(text=text, lang=lg, slow=slow_option)
    
    try:
        my_file_name = text[0:20].replace(" ", "_")
    except:
        my_file_name = "audio"
    
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    
    return file_path



# BOTÓN GENERAR AUDIO


if st.button("▶ Generar Audio"):

    if text.strip() == "":
        st.warning("Por favor ingresa un texto antes de generar el audio.")
    else:
        file_path = text_to_speech(text, lg, slow_option)

        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()

        st.markdown("### 🎵 Tu audio:")
        st.audio(audio_bytes, format="audio/mp3")

        # Descargar archivo
        b64 = base64.b64encode(audio_bytes).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="audio.mp3">⬇ Descargar audio</a>'
        st.markdown(href, unsafe_allow_html=True)


# LIMPIAR ARCHIVOS ANTIGUOS


def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
