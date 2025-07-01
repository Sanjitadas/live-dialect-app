# streamlit_ui.py

import streamlit as st
import threading
from utils.languages import supported_languages
from utils.tts import speak_text
from live_dialect import start_translation_pipeline

# Build searchable dropdown list
language_options = [f'{lang["name_en"]} ({lang["native"]})' for lang in supported_languages]
language_name_to_code = {f'{lang["name_en"]} ({lang["native"]})': lang["code"] for lang in supported_languages}

# Voice style dictionary
voice_styles = {
    "en": ["Male (US)", "Female (US)", "Male (UK)", "Female (UK)", "Male (India)", "Female (India)"],
    "hi": ["Male", "Female"],
    "es": ["Male (Spain)", "Female (Spain)"],
    "fr": ["Male", "Female"],
    "zh-CN": ["Male", "Female"],
    "ar": ["Male", "Female"],
}

st.set_page_config(page_title="🌐 Live Dialect Translator", layout="centered")
st.title("🗣️ AI Dialect Translator with Voice Preview")

st.markdown("### 🌐 Choose Languages")

col1, col2 = st.columns(2)
with col1:
    input_lang_display = st.selectbox("🎤 Input Language", language_options, index=language_options.index("English (English)"))
    input_lang = language_name_to_code[input_lang_display]

with col2:
    output_lang_display = st.selectbox("🗣️ Output Language", language_options, index=language_options.index("English (English)"))
    output_lang = language_name_to_code[output_lang_display]

# 🎧 Voice Style Options
available_voices = voice_styles.get(output_lang, ["Default Male", "Default Female"])
voice_choice = st.selectbox("🎧 Voice Style", available_voices)

# 🔊 Voice Preview Button
preview_text = st.text_input("🔈 Preview TTS Text", value="Hello! This is a sample voice preview.")
if st.button("▶️ Play Voice Preview"):
    st.info("Playing preview...")
    speak_text(preview_text, lang=output_lang, engine="edge", voice_style=voice_choice)

# 🚀 Launch Live Translation
if st.button("🚀 Start Real-Time Translation"):
    st.success(f"Translation started: {input_lang_display} → {output_lang_display} using {voice_choice}")
    threading.Thread(
        target=start_translation_pipeline,
        args=(input_lang, output_lang, voice_choice),
        daemon=True
    ).start()

