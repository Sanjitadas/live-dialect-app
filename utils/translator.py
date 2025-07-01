import os
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def translate_text(text, input_lang="en", output_lang="en"):
    prompt = f"Translate the following sentence from {input_lang} English to fluent {output_lang} English with grammar correction:\n\n{text}"

    response = co.chat(
        model="command-r",
        message=prompt
    )
    return response.text

