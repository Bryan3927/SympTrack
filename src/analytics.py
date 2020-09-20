import pandas as pd
import matplotlib.pyplot as plt
import os

from .db import find_data_for_symptom


def build_figure(username, symptom):
    data = find_data_for_symptom(username, symptom)
    df = pd.DataFrame(data, columns=['username', 'symptom', 'date', 'time', 'severity', 'notes'])
    df = df.sort_values('date')
    df = df.reset_index(drop=True)

    plt.plot(df['date'], df['severity'])
    plt.xlabel('date')
    plt.ylabel('severity')

    filename = f'{username}-{symptom}.png'
    filepath = f'{os.getcwd()}/static/images/{filename}'

    plt.savefig(filepath)
    plt.close()

    return filename

# TODO: THIS IS ACTUALLY REALLY BAD / RUDIMENTARY, BUT IT WORKS; MIGHT FIX IN FUTURE
