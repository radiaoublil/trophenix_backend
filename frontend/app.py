import streamlit as st
from audiorecorder import audiorecorder
import requests
import tempfile

BACKEND_URL = "http://127.0.0.1:8000"  # à adapter si ton API est déployée ailleurs

st.title("🎤 Générateur de CV Trophenix")
st.markdown("Parle et laisse l’IA créer ton CV ! 🧠")

# ----------------------------
# 1️⃣ Infos utilisateur
# ----------------------------
name = st.text_input("Nom complet")
email = st.text_input("Adresse email")

# ----------------------------
# 2️⃣ Enregistrement vocal 🎙️
# ----------------------------
st.header("🎙️ Enregistre ton message vocal")

audio = audiorecorder("Démarrer l’enregistrement", "Arrêter l’enregistrement")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")
    st.success("✅ Enregistrement terminé")

    if st.button("Transcrire l’audio 📝"):
        with st.spinner("Transcription en cours..."):
            # Sauvegarde temporaire du fichier audio
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                audio.export(tmp.name, format="wav")
                tmp_path = tmp.name

            files = {"audio": open(tmp_path, "rb")}
            data = {"name": name, "email": email}
            response = requests.post(f"{BACKEND_URL}/transcribe_audio", files=files, data=data)

        if response.status_code == 200:
            result = response.json()
            st.success("Transcription terminée ✅")
            st.session_state["transcript"] = result["transcript"]
        else:
            st.error(f"Erreur {response.status_code}: {response.text}")

# ----------------------------
# 3️⃣ Correction manuelle
# ----------------------------
if "transcript" in st.session_state:
    st.header("🖋️ Vérifie et corrige ton texte")
    corrected_text = st.text_area("Texte corrigé :", value=st.session_state["transcript"], height=200)
    st.session_state["corrected_text"] = corrected_text

# ----------------------------
# 4️⃣ Génération du CV
# ----------------------------
if "corrected_text" in st.session_state:
    if st.button("Générer le CV 📄"):
        with st.spinner("Génération du CV..."):
            response = requests.post(
                f"{BACKEND_URL}/generate_cv_from_text",
                data={
                    "name": st.session_state.get("name", "Utilisateur inconnu"),
                    "email": st.session_state.get("email", "inconnu@example.com"),
                    "message": st.session_state["corrected_text"]
                }
            )


        if response.status_code == 200:
            result = response.json()
            st.success("CV généré avec succès 🎉")

            st.json(result["cv_json"])

            cv_path = result["cv_path"]
            with open(cv_path, "rb") as f:
                st.download_button("⬇️ Télécharger le CV", f, file_name="cv.docx")

        else:
            st.error(f"Erreur {response.status_code} : {response.text}")
