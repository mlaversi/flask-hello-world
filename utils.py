# First test : Receive the audio and output the lenght of the output OK
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import io
import openai 
# Second : 

#Métriques : Liau Coleman : 

# def coleman_liau_index(text, language):
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use 'text-davinci-003' for ChatGPT Turbo
#         prompt=f"In {language}, please only give me the coleman liau index from the following text. The input text is: {text}",
#         max_tokens=100
#     )
#     return response.choices[0].text 

def generate_audio_plot(samples, duration):
    # Créer une figure avec deux sous-graphiques côte à côte
    fig, ax = plt.subplots(figsize=(15, 4))

    # Premier sous-graphique : signal audio dans le domaine temporel
    time = np.linspace(0., duration, len(samples))
    ax.plot(time, samples)
    ax.set(xlabel="Temps (s)", ylabel="Amplitude", title="Signal Audio dans le Domaine Temporel")

    # Sauvegarder la figure dans un buffer
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)

    return output
