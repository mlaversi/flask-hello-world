from flask import Flask, request, jsonify
import pandas as pd 
from google.cloud import speech_v1p1beta1 as speech


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'COUCOU, TRIPLE MONSTRE BROTHER' 

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
def upload_audio():
    if 'audio' not in request.files:
        return 'Aucun fichier audio dans la requête', 400

    audio_file = request.files['audio']

    # Traitez le fichier audio ici selon vos besoins.
    # Par exemple, vous pouvez le sauvegarder sur le serveur et effectuer des transformations.

    # Simulons une transformation en ajoutant un préfixe au texte
    transformed_audio = "Transformed: " + audio_file.read().decode('utf-8')

    # Simulons des métriques
    metrics = {'duration': 120, 'size': len(transformed_audio)}

    # Retournez les données traitées à FlutterFlow
    response_data = {'transformed_audio': transformed_audio, 'metrics': metrics}
    
    return jsonify(response_data), 200
@app.route('/testaudio', methods=['POST'])
def get_audio_text():
    try:
        # Read audio bytes from the request
        audio_bytes = request.get_data()

        # Initialize Google Cloud Speech client
        client = speech.SpeechClient()

        # Create a recognition config
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=44100,
            language_code="en-US",
        )

        # Convert audio bytes to Audio data
        audio = speech.RecognitionAudio(content=audio_bytes)

        # Perform speech recognition
        response = client.recognize(config=config, audio=audio)

        # Extract transcribed text
        text = response.results[0].alternatives[0].transcript

        # Get the size of the audio (replace this logic with your own logic)
        audio_size = len(audio_bytes)

        # Return the audio size and transcribed text in JSON format
        return jsonify({'audioSize': audio_size, 'transcribedText': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For running the app locally
if __name__ == '__main__':
    app.run()
    
