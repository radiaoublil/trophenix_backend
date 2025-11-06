import os
import json
from google import genai
from app.utils.prompt import CV_EXTRACTION_PROMPT

API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD3DHfwxF6S2aTMqpfmyXkbkSzOTDryskE")
client = genai.Client(api_key=API_KEY)

def generate_cv_json(final_message):
    prompt = CV_EXTRACTION_PROMPT.format(texte=final_message)

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
        config={"temperature": 0.2, "max_output_tokens": 1000},
    )

    output_text = response.text.strip()

    # Nettoyage si JSON encapsulé dans ```
    if output_text.startswith("```json"):
        output_text = output_text.replace("```json", "").replace("```", "").strip()

    try:
        cv_data = json.loads(output_text)
        return cv_data
    except json.JSONDecodeError:
        raise ValueError("⚠️ Le modèle n’a pas renvoyé un JSON valide.")
