import numpy as np
from ClassifierAbstract import ClassifierAbstract


class NormalDistributionClassifier(ClassifierAbstract):
    def __init__(self):
        self._mean = 0.0
        self._revert_sd = 0.0
        self._sd = 0.0

    def fit(self, data):
        self._mean = np.mean(data)
        self._sd = np.std(data)
        self._revert_sd = 1/self._sd

    def predict(self, value):
        # print(abs((self._mean - float(value)) * self._revert_sd))
        return (abs(self._mean - float(value[0])) * self._revert_sd) < 3

    def get_model_params(self):
        return '{' + '"model": "Gausian", "mean": {mean}, "standard_deviation": {sd}'.format(mean=self._mean, sd=self._sd) + '}'
