from flask import Flask, request, jsonify, send_file
import pandas as pd 
from pydub import AudioSegment
import random 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import base64
from utils import *
import zipfile
from PIL import Image
from io import BytesIO
import librosa
import speech_recognition as sr
import os 

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'COUCOU, Quadruple MONSTRE BROTHER' 

# Création des données fictives
data = {
    'Nom': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],
    'Age': [25, 30, 22, 35, 28]
}
# Création du DataFrame
df = pd.DataFrame(data)

@app.route('/dataframe')
def get_dataframe():
    # Convertir le DataFrame en format JSON
    dataframe_json = df.to_json(orient='records', default_handler=str)
    return jsonify({'dataframe': dataframe_json})

###IMAGES
@app.route('/testimages', methods=['POST'])
def get_audio_images():
    try:
        # Lire les bytes de l'audio depuis la requête
        audio_bytes = request.get_data()

        # Convertir les bytes en un objet AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # Obtenir les échantillons et la durée
        samples = np.array(audio.get_array_of_samples())
        duration = len(audio) / 1000.0  # Durée en secondes

        # Générer le graphique audio
        plot_bytes = generate_audio_plot(samples, duration)

        # Créer un fichier zip contenant l'image
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('audio_plot.png', plot_bytes.getvalue())

        # Retourner le fichier zip
        zip_buffer.seek(0)
        return send_file(zip_buffer, mimetype='application/zip', as_attachment=True, download_name='audio_plots.zip')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

### FREQUENCES, TAILLE, RANDOM Number
@app.route('/testaudio', methods=['POST'])
def get_audio_infos():
    try:
        # Lire les bytes de l'audio depuis la requête
        audio_bytes = request.get_data()

        # Convertir les bytes en un objet AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # Obtenir la fréquence de l'audio
        audio_frequency = audio.frame_rate

        # Obtenir la taille de l'audio
        audio_size = len(audio_bytes)

        # Générer un nombre aléatoire
        random_number = random.randint(1, 100)

        # Retourner les informations au format JSON
        return jsonify({'audioFrequency': audio_frequency, 'audioSize': audio_size, 'randomNumber': random_number})

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/analyse-audio', methods=['POST'])
def analyse_audio():
    # Vérifier si un fichier audio est attaché à la requête
    if 'audio' not in request.files:
        return jsonify({'error': 'Aucun fichier audio attaché à la requête'}), 400

    fichier_audio = request.files['audio']

    # Vérifier si le fichier a une extension audio (ajuster selon vos besoins)
    if not fichier_audio.filename.endswith(('.mp3', '.wav', '.ogg')):
        return jsonify({'error': 'Le fichier doit être au format MP3, WAV ou OGG'}), 400

    # Charger le fichier audio avec librosa
    try:
        audio, _ = librosa.load(fichier_audio, sr=None)
    except Exception as e:
        return jsonify({'error': f'Erreur lors du chargement du fichier audio : {str(e)}'}), 500

    # Utiliser un module de reconnaissance vocale (SpeechRecognition)
    recognizer = sr.Recognizer()
    with sr.AudioFile(fichier_audio) as source:
        audio_data = recognizer.record(source)

    # Convertir le texte à partir du fichier audio
    try:
        texte_reconnu = recognizer.recognize_google(audio_data, language='fr-FR')
    except sr.UnknownValueError:
        texte_reconnu = "Aucun texte n'a pu être reconnu"
    except sr.RequestError as e:
        texte_reconnu = f"Erreur lors de la demande de reconnaissance vocale : {str(e)}"

    return jsonify({'texte_reconnu': texte_reconnu}), 200



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
            audio_path = "uploaded_audio.wav"
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




# ### Images transformation. 
# def convert_to_black_and_white(image):
#     # Ouvrir l'image en utilisant la bibliothèque PIL
#     img = Image.open(BytesIO(image))

#     # Convertir l'image en tableau numpy
#     img_array = np.array(img)

#     # Appliquer la conversion en noir et blanc
#     img_bw = Image.fromarray(np.dot(img_array[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8))

#     # Convertir l'image en tableau de bytes
#     img_bytes = BytesIO()
#     img_bw.save(img_bytes, format="PNG")
#     img_bytes = img_bytes.getvalue()

#     return img_bytes

# @app.route('/transform', methods=['POST'])
# def transform_image():
#     try:
#         # Récupérer l'image depuis la requête POST
#         image = request.files['image'].read()

#         # Appeler la fonction de conversion en noir et blanc
#         transformed_image = convert_to_black_and_white(image)

#         # Retourner l'image transformée
#         return jsonify({'status': 'success', 'image': str(transformed_image)})

#     except Exception as e:
#         return jsonify({'status': 'error', 'message': str(e)})

# For running the app locally
if __name__ == '__main__':
    app.run()
    
