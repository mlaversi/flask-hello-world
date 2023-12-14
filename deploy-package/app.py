from flask import Flask, request, jsonify
import pandas as pd
import speech_recognition as sr
import os

app = Flask(__name__)

# Création des données fictives
data = {
    'Nom': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],
    'Age': [25, 30, 22, 35, 28]
}
# Création du DataFrame
df = pd.DataFrame(data)

@app.route('/')
def hello_world():
    return 'COUCOU, Quadruple MONSTRE BROTHER'

@app.route('/dataframe')
def get_dataframe():
    # Convertir le DataFrame en format JSON
    dataframe_json = df.to_json(orient='records', default_handler=str)
    return jsonify({'dataframe': dataframe_json})

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_sphinx(audio_data)
            return text
        except sr.UnknownValueError:
            return "La reconnaissance vocale n'a pas pu comprendre l'audio."
        except sr.RequestError as e:
            return f"Erreur lors de la demande de reconnaissance vocale : {e}"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        audio_file = request.files['audio']
        if audio_file and audio_file.filename.endswith('.wav'):
            # Enregistrez le fichier audio
            audio_path = "uploaded_audio.mp3"
            audio_file.save(audio_path)

            # Transcrire le fichier audio
            transcribed_text = transcribe_audio(audio_path)

            # Supprimez le fichier audio après la transcription
            os.remove(audio_path)

            return jsonify({"transcribed_text": transcribed_text})
        else:
            return jsonify({"error": "Veuillez fournir un fichier audio au format WAV."})
    except Exception as e:
        return jsonify({"error": f"Une erreur s'est produite : {str(e)}"})

# For running the app locally
if __name__ == '__main__':
    app.run()
