import os
from app.features.record_message import record_audio, correct_text, save_message
from app.features.transcription import transcribe_audio
from app.features.gemini_service import generate_cv_json

def main():
    print("=== Générateur de CV Trophenix ===")
    print("1️⃣ Écrire un message")
    print("2️⃣ Parler pour enregistrer un message")
    choice = input("➡️ Entrez 1 ou 2 : ").strip()

    if choice == "1":
        final_message = input("✏️ Écrivez votre message :\n")
    elif choice == "2":
        audio_path = record_audio()
        transcription = transcribe_audio(audio_path)
        final_message = correct_text(transcription)
        os.remove(audio_path)
    else:
        print("❌ Choix invalide")
        return

    save_message(final_message)

    # Génération du JSON
    print("\n🧠 Envoi à Gemini pour structuration du CV...")
    try:
        cv_data = generate_cv_json(final_message)
        print("✅ CV structuré généré avec succès !\n")
        print(cv_data)
    except Exception as e:
        print("❌ Erreur lors de la génération :", e)

if __name__ == "__main__":
    main()
