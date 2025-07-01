import tkinter as tk

class SubtitleOverlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Translation")
        self.root.geometry("800x150+100+100")
        self.root.configure(bg="black")
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.85)
        self.root.overrideredirect(True)

        self.label = tk.Label(self.root, text="", fg="white", bg="black", font=("Helvetica", 22))
        self.label.pack(expand=True)

    def update_text(self, text):
        self.label.config(text=text)
        self.root.update()

    def close(self):
        self.root.destroy()


