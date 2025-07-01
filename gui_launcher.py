import tkinter as tk
from tkinter import ttk
from utils.languages import supported_languages
from utils.voices import available_voices
from live_dialect import start_translation_pipeline

def launch_gui():
    # Mp language name to codes
    lang_code_map = {lang['name_en']: lang['code'] for lang in supported_languages}

    def on_start():
        input_lang = lang_code_map[input_lang_var.get()]
        output_lang = lang_code_map[output_lang_var.get()]
        voice_style = voice_var.get()
        root.destroy()
        start_translation_pipeline(input_lang, output_lang, voice_style)

    root = tk.Tk()
    root.title("Live Dialect Translator")
    root.geometry("500x300")

    ttk.Label(root, text="🎤 Input Language:").pack(pady=5)
    input_lang_var = tk.StringVar()
    input_dropdown = ttk.Combobox(root, textvariable=input_lang_var)
    input_dropdown['values'] = [l['name_en'] for l in supported_languages]
    input_dropdown.pack()

    ttk.Label(root, text="🗣 Output Language:").pack(pady=5)
    output_lang_var = tk.StringVar()
    output_dropdown = ttk.Combobox(root, textvariable=output_lang_var)
    output_dropdown['values'] = [l['name_en'] for l in supported_languages]
    output_dropdown.pack()

    ttk.Label(root, text="🎧 Voice Style:").pack(pady=5)
    voice_var = tk.StringVar()
    voice_dropdown = ttk.Combobox(root, textvariable=voice_var)
    voice_dropdown['values'] = available_voices
    voice_dropdown.set("Default Male")
    voice_dropdown.pack()

    tk.Button(root, text="▶ Start Translation", command=on_start).pack(pady=20)
    root.mainloop()

# Run when file is executed
if __name__ == "__main__":
    launch_gui()
