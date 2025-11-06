import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import tempfile
import os

FS = 44100  # fréquence d’échantillonnage

def record_audio(fs=FS):
    print("🎙️ Enregistrement... Appuyez sur Entrée pour arrêter.")

    frames = []
    sd.default.samplerate = fs
    sd.default.channels = 1

    def callback(indata, frames_count, time_info, status):
        frames.append(indata.copy())

    stream = sd.InputStream(callback=callback)
    stream.start()

    input()  # Attendre que l'utilisateur appuie sur Entrée pour stopper
    stream.stop()

    print("✅ Enregistrement terminé")

    audio = np.concatenate(frames, axis=0)
    
    tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmpfile.name, fs, (audio * 32767).astype(np.int16))

    return tmpfile.name

def correct_text(transcription):
    print("\n📝 Transcription générée :")
    print(transcription)
    print("\n✏️ Vous pouvez corriger la transcription ci-dessous.")
    correction = input("➡️ Modifiez si besoin (ou appuyez sur Entrée si OK) :\n")
    return correction if correction.strip() else transcription

def save_message(message, file_path="data/messages.txt"):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")
    print("✅ Message enregistré :", message)
