from sklearn.datasets import make_classification
from sklearn.manifold import TSNE
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import OneClassSVM
from ClassifierAbstract import ClassifierAbstract
import numpy as np
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions

def plot_2d(data):
    x = data[:, 1] * 1/3600
    y = data[:, 2]
    plt.plot(x, y, 'o')
    plt.show()


class OneClassSVMClassifier(ClassifierAbstract):
    def __init__(self):
        self._model = OneClassSVM()

    def fit(self, data):
        train, test = train_test_split(data, test_size=0.33)
        self._model.fit(train)
        print(self._model.predict(data))
        test_y = (test.reshape(-1) * 0) + 1
        # print(f1_score(test, test_y, pos_label=1))

    def predict(self, value):
        y = self._model.score_samples([value])
        print(y[0])
        y = self._model.predict([value])
        print(y[0])
        return 1
