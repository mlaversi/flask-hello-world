from flask import Flask, request, jsonify
import pandas as pd 
from pydub import AudioSegment
import io
import random 
import matplotlib.pyplot as plt
import numpy as np

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


@app.route('/upload', methods=['POST'])
def upload_and_analyze():
    try:
        # Lire les bytes de l'audio depuis la requête
        audio_bytes = request.get_data()

        # Convertir les bytes en un objet AudioSegment
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

        # Obtenir les données pour l'analyse spectrale
        samples = np.array(audio.get_array_of_samples())

        # Effectuer l'analyse spectrale (exemple : spectrogramme)
        plt.specgram(samples, Fs=audio.frame_rate)

        # Enregistrer le tracé dans un tableau en bytes
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        # Retourner l'image sous forme d'un tableau en bytes
        return jsonify({'spectrogram': img_buf.read().decode('latin1')})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/testaudio', methods=['POST'])
def get_audio_info():
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


# For running the app locally
if __name__ == '__main__':
    app.run()
    
