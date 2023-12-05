from flask import Flask, request, jsonify, send_file
import pandas as pd 
from pydub import AudioSegment
import io
import random 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import base64
from utils import *

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
def get_audio_info():
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

        # Retourner l'image au format JPEG
        return send_file(io.BytesIO(plot_bytes.getvalue()), mimetype='image/png')

    except Exception as e:
        return jsonify({'error': str(e)}), 500

### FREQUENCES, TAILLE, RANDOM NUMBER

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
    
