from ClassifierAbstract import ClassifierAbstract
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import IsolationForest


def plot_3(data):
    x = data[:, 0]
    x[x == 0] = 7
    y = data[:, 1] * (1 / 3600)
    z = data[:, 2]
    print(z)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax = plt.axes(projection='3d')
    ax.scatter(x, z, y)
    plt.show()


class IsolationForestClassifier(ClassifierAbstract):
    def __init__(self):
        self._model = None
        self._contamination = 0.001
        self._max_samples = 256

    def set_model(self, options):
        if 'contamination' in options:
            self._contamination = options['contamination']
        if 'max_samples' in options:
            self._max_samples = options['max_samples']  # Maximum samples from sklearn

    def fit(self, data):
        self._max_samples = len(data) - 1
        self._model = IsolationForest(contamination=self._contamination, max_samples=self._max_samples)
        self._model.fit(data)

    def predict(self, value):
        state = self._model.predict([value])[0]
        return state > 0

    def get_model_params(self):
        return '{' + '"model": "Isolation forest" , "contamination": {contamination}'.format(contamination=self._contamination) +'}'
