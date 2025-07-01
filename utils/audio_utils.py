import speech_recognition as sr
import os
from pydub import AudioSegment
import tkinter as tk
from tkinter import filedialog

def adjust_mic_sensitivity(threshold=300):
    r = sr.Recognizer()
    r.energy_threshold = threshold
    return r

def transcribe_audio_file(file_path, lang="en"):
    r = adjust_mic_sensitivity()
    audio_format = os.path.splitext(file_path)[1].lower()

    if audio_format not in [".mp3", ".mp4", ".wav"]:
        raise ValueError("Unsupported format. Use MP3, MP4, or WAV.")

    sound = AudioSegment.from_file(file_path)
    sound.export("temp.wav", format="wav")

    with sr.AudioFile("temp.wav") as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio, language=lang)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error with Google STT: {e}"

def choose_audio_file():
    root = tk.Tk()
    root.withdraw()  # Hide main window
    file_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=[("Audio Files", "*.wav *.mp3 *.mp4")]
    )
    return file_path

