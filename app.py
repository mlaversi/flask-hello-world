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


### Images transformation. 
def convert_to_black_and_white(image):
    # Ouvrir l'image en utilisant la bibliothèque PIL
    img = Image.open(BytesIO(image))

    # Convertir l'image en tableau numpy
    img_array = np.array(img)

    # Appliquer la conversion en noir et blanc
    img_bw = Image.fromarray(np.dot(img_array[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8))

    # Convertir l'image en tableau de bytes
    img_bytes = BytesIO()
    img_bw.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    return img_bytes

@app.route('/transform', methods=['POST'])
def transform_image():
    try:
        # Récupérer l'image depuis la requête POST
        image = request.files['image'].read()

        # Appeler la fonction de conversion en noir et blanc
        transformed_image = convert_to_black_and_white(image)

        # Retourner l'image transformée
        return jsonify({'status': 'success', 'image': str(transformed_image)})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# For running the app locally
if __name__ == '__main__':
    app.run()
    
