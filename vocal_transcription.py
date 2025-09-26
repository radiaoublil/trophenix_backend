import sounddevice as sd
import numpy as np
import whisper
import tempfile
import os
from scipy.io.wavfile import write

FS = 16000
DURATION = 30
MODEL_NAME = "base"

model = whisper.load_model(MODEL_NAME)

def record_audio(duration=DURATION, fs=FS):
    print("🎙️ Enregistrement... Parlez maintenant")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    print("✅ Enregistrement terminé")

    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmpfile.name, fs, (audio * 32767).astype(np.int16))
    return tmpfile.name

def transcribe_audio(path):
    print("⏳ Transcription en cours...")
    result = model.transcribe(path, language="fr")
    return result["text"]

def correct_text(transcription):
    print("\n📝 Transcription générée :")
    print(transcription)
    print("\n✏️ Vous pouvez éditer la transcription ci-dessous.")
    correction = input("➡️ Modifiez si besoin (ou appuyez sur Entrée si OK) :\n")
    return correction if correction.strip() else transcription

def save_message(message, file_path="messages.txt"):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print("✅ Message enregistré :", message)

def main():
    print("Choisissez une option :")
    print("1. Écrire un message")
    print("2. Parler pour générer un message")
    choice = input("➡️ Entrez 1 ou 2 : ").strip()

    if choice == "1":
        # Saisie texte
        final_message = input("✏️ Écrivez votre message :\n")
    elif choice == "2":
        # Enregistrement et transcription
        audio_path = record_audio()
        transcription = transcribe_audio(audio_path)
        final_message = correct_text(transcription)
        os.remove(audio_path)
    else:
        print("❌ Choix invalide")
        return

    save_message(final_message)

if __name__ == "__main__":
    main()
