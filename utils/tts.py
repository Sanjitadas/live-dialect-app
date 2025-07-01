import edge_tts
import asyncio
import pyttsx3

# Voice style map per language
DEFAULT_VOICE_BY_LANG = {
    "en": "en-US-GuyNeural",
    "hi": "hi-IN-MadhurNeural",
    "bn": "bn-IN-TanishaaNeural",
    "ta": "ta-IN-ValluvarNeural",
    "te": "te-IN-MohanNeural",
    "mr": "mr-IN-AarohiNeural",
    "gu": "gu-IN-DhwaniNeural",
    # Add more if needed
}

async def _speak_edge(text, lang="en", voice_style=None):
    voice = voice_style or DEFAULT_VOICE_BY_LANG.get(lang[:2], "en-US-GuyNeural")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.stream()

def speak_text(text, lang="en", engine="edge", voice_style=None):
    if engine == "edge":
        asyncio.run(_speak_edge(text, lang=lang, voice_style=voice_style))
    else:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()



