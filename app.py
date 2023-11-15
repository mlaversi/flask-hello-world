from flask import Flask, request, jsonify
import pandas as pd 

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'COUCOU, TRIPLE MONSTRE BROTHER' 

data = {
    'Nom': ['Alice', 'Bob', 'Charlie', 'David', 'Emma'],
    'Âge': [25, 30, 22, 35, 28]
}
df = pd.DataFrame(data)

# Endpoint pour retourner le DataFrame
@app.route('/dataframe')
def get_dataframe():
    try:
        # Convertir le DataFrame en format JSON en gérant les caractères Unicode
        dataframe_json = df.to_json(orient='records', default=str)

        return jsonify({'dataframe': dataframe_json})
    except Exception as e:
        return str(e), 500  # Retourne le message d'erreur et un code d'état 500

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

# For running the app locally
if __name__ == '__main__':
    app.run()
    
