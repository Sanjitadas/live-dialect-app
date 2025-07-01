# api.py

from flask import Flask, request, jsonify
from utils.grammar import correct_grammar
from utils.translator import translate_text
from utils.tts import speak_text
from utils.languages import get_language_code
from os import getenv


app = Flask(__name__)
app.run(host="0.0.0.0", port=int(getenv("PORT", 5000)), debug=True)

@app.route("/")
def health():
    return "✅ Live Dialect Translator API is up!"

@app.route("/api/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")
    input_lang = get_language_code(data.get("input_lang", "Indian English"))
    output_lang = get_language_code(data.get("output_lang", "US English"))
    voice_style = data.get("voice_style", "Auto")

    corrected = correct_grammar(text)
    translated = translate_text(corrected, input_lang, output_lang)

    try:
        speak_text(translated, lang=output_lang, voice_style=voice_style)
    except Exception as e:
        print("[TTS Error]", e)

    return jsonify({
        "corrected": corrected,
        "translated": translated
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
