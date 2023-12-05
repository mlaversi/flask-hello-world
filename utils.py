# First test : Receive the audio and output the lenght of the output OK
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
# Second : 

#Sortir métriques audio (intensité vis à vis des fréquences)
#Envoyer les fréquences

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
