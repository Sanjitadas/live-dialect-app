# web_app.py

import streamlit as st
from utils.stt import capture_streaming
from utils.grammar import correct_grammar
from utils.translator import translate_text
from utils.tts import speak_text
from utils.languages import get_language_code
import os

st.set_page_config(page_title="Dialect Translator", layout="centered")

st.title("🗣️ Live Indian English to US English Translator")

# Dropdowns for selecting input and output languages
input_lang = st.selectbox("🔤 Input Language", ["Indian English", "Hindi", "Telugu", "Tamil", "Gujarati", "Marathi"])
output_lang = st.selectbox("🌍 Output Language", ["US English", "Hindi", "Telugu", "Tamil", "Gujarati", "Marathi"])

# Voice style choice
voice_style = st.radio("🔈 Voice Style", ["Auto", "Male (US)", "Female (India)"], index=0)

# Button to start translation
if st.button("▶️ Start Live Translation"):

    input_code = get_language_code(input_lang)
    output_code = get_language_code(output_lang)

    st.success("🎤 Listening... You can speak now. Press Ctrl+C in terminal to stop.")

    def handle_transcribed_text(text):
        st.write(f"📝 Recognized: `{text}`")
        corrected = correct_grammar(text)
        st.write(f"✍️ Corrected: `{corrected}`")
        translated = translate_text(corrected, input_code, output_code)
        st.write(f"🌐 Translated: `{translated}`")

        if voice_style == "Auto":
            speak_text(translated, lang=output_code)
        else:
            speak_text(translated, lang=output_code, voice_style=voice_style)

    capture_streaming(handle_transcribed_text, lang=input_code)
