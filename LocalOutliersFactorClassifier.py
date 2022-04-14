from sklearn.neighbors import LocalOutlierFactor
from ClassifierAbstract import ClassifierAbstract
from sklearn.model_selection import train_test_split


class LocalOutliersFactorClassifier(ClassifierAbstract):
    def __init__(self):
        self._model = None
        self._contamination = 0.01
        self._n_neighbors = 30
        self._acc = 0.0

    def fit(self, data):
        self._model = LocalOutlierFactor(novelty=True, n_neighbors=self._n_neighbors, contamination=self._contamination)
        data_train, data_test, = train_test_split(data, test_size=0.33)

        self._model.fit(data_train)
        y_pred = self._model.predict(data_test)

        cnt = 0
        for i in range(0, len(y_pred)):
            if y_pred[i] == -1:
                cnt = cnt + 1
        self._acc = (1-(cnt/len(data_test))) * 100

    def predict(self, value):
        state = self._model.predict([value])[0]
        return state > 0

    def get_model_params(self):
        return '{' + '"model": "Local outliers factor", "contamination": {}, "neighbors": {}, "accurancy": {:.3f}'.format(self._contamination, self._n_neighbors, self._acc) + '}'

    def set_model(self, options):
        if 'contamination' in options:
            self._contamination = options['contamination']
        if 'n_neighbors' in options:
            self._n_neighbors = options['n_neighbors']  # Maximum samples from sklearn
