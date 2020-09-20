import pandas as pd
import matplotlib.pyplot as plt
import os

from.db import find_data_for_symptom


def build_figure(username, symptom):
    print('AAAAAAA')
    print(os.getcwd())
    data = find_data_for_symptom(username, symptom)
    df = pd.DataFrame(data, columns=['username', 'symptom', 'date', 'time', 'severity', 'notes'])
    filename = f'{username}-{symptom}.png'
    plt.plot(df['date'], df['severity'])
    plt.xlabel('date')
    plt.ylabel('severity')
    plt.savefig(f'{os.getcwd()}/static/images/{filename}')

    return filename

# TODO: THIS IS ACTUALLY REALLY BAD / RUDIMENTARY, BUT IT WORKS; MIGHT FIX IN FUTURE
