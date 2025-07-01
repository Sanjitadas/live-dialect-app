import argparse
import threading
import os
from datetime import datetime

from utils.stt import capture_streaming
from utils.grammar import correct_grammar
from utils.translator import translate_text
from utils.tts import speak_text
from subtitle_overlay import SubtitleOverlay
from utils.file_utils import save_transcript
from utils.languages import get_language_code


def start_translation_pipeline(input_lang, output_lang, voice_style="Default Male", bidirectional=False):
    overlay = SubtitleOverlay()

    # Start the subtitle overlay in the main thread to avoid Tcl threading issue
    threading.Thread(target=overlay.run, daemon=True).start()

    transcripts = []

    def on_stream(text):
        print(f"\n📝 Live Recognized: {text}")
        corrected = correct_grammar(text)
        print(f"✍️ Corrected: {corrected}")

        translated = translate_text(corrected, input_lang, output_lang)
        print(f"🗣️ Output ({output_lang}): {translated}")

        speak_text(translated, lang=output_lang, engine="edge", voice_style=voice_style)
        overlay.update_text(translated)

        timestamp = datetime.now().strftime("%H:%M:%S")
        transcripts.append(f"{timestamp} - {translated}")

        # Bidirectional swap
        nonlocal input_lang, output_lang
        if bidirectional:
            input_lang, output_lang = output_lang, input_lang

    try:
        # Live microphone streaming
        capture_streaming(callback=on_stream, lang=input_lang)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
        overlay.close()
        save_transcript(transcripts)


def translate_audio_file(path, input_lang, output_lang, voice_style="Default Male"):
    from utils.stt import transcribe_audio_file

    print(f"🎧 Transcribing file: {path}")
    text = transcribe_audio_file(path, input_lang)
    print(f"📝 Transcribed: {text}")

    corrected = correct_grammar(text)
    print(f"✍️ Corrected: {corrected}")

    translated = translate_text(corrected, input_lang, output_lang)
    print(f"🗣️ Output ({output_lang}): {translated}")

    speak_text(translated, lang=output_lang, engine="edge", voice_style=voice_style)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="Input language name", default="english")
    parser.add_argument("--output", help="Output language name", default="hindi")
    parser.add_argument("--voice", help="Voice style (e.g., 'Default Male')", default="Default Male")
    parser.add_argument("--bidirectional", action="store_true", help="Enable bidirectional translation toggle")
    parser.add_argument("--file", help="Translate uploaded audio file (MP3/MP4/WAV)")
    args = parser.parse_args()

    input_lang = get_language_code(args.input)
    output_lang = get_language_code(args.output)

    if args.file:
        translate_audio_file(args.file, input_lang, output_lang, args.voice)
    else:
        start_translation_pipeline(
            input_lang=input_lang,
            output_lang=output_lang,
            voice_style=args.voice,
            bidirectional=args.bidirectional
        )





