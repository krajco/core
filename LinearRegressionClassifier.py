import matplotlib.pyplot as plt
import numpy as np

from math import sqrt
from datetime import datetime
from datetime import timedelta
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import matplotlib .dates as mdates

from time import strftime
from time import gmtime

from ClassifierAbstract import ClassifierAbstract


def plot_data(data, data_x, data_y, predicted):
    x = data_x.reshape(-1)
    y = data_y
    index = 30
    # date = [str(strftime('%H:%M', gmtime(elem))) for elem in x]
    # xx = [datetime.strptime(elem, '%H:%M') for elem in date]
    date = [str(datetime.fromtimestamp(elem)) for elem in x]
    xx = [datetime.strptime(elem, '%Y-%m-%d %H:%M:%S') for elem in date]
    my_fmt = mdates.DateFormatter('%d')

    plt.scatter(xx[::index], y[::index])
    # plt.plot(xx[::index], predicted[::index], color='red')
    plt.xticks(rotation=45)
    plt.ylabel('Energy [kWh]')
    plt.xlabel('Time')
    plt.ylim(300, 350)
    plt.show()


class LinearRegressionClassifier(ClassifierAbstract):
    def __init__(self):
        self._model = LinearRegression()
        self._mse = self._rmse =self._r2_score = self._standard_deviation = None

    def fit(self, data):
        data_x = data[:, 0].reshape(-1, 1)
        data_y = data[:, 1]

        data_x = data_x[::3]
        data_y = data_y[::3]

        data_x_train, data_x_test, data_y_train, data_y_test = train_test_split(data_x, data_y, test_size=0.33)

        self._model.fit(data_x_train, data_y_train)
        data_y_predict = self._model.predict(data_x_test)

        self._mse = mean_squared_error(data_y_test, data_y_predict)
        self._rmse = mean_squared_error(data_y_test, data_y_predict, squared=False)
        self._r2_score = r2_score(data_y_test, data_y_predict)
        self._standard_deviation = sqrt(self._mse)
#        result = self._model.predict(data_x_train)
#        plot_data(data, data_x_train, data_y_train, result)

    def predict(self, value):
        value = np.array(value)
        x = value[0]
        y = value[1]
        err = abs(y - self._model.predict([[x]])[0])
        return err < 3 * self._standard_deviation

    def print_stats(self):
        print('Coefficients: ' + str(self._model.coef_[0]))
        print('Intercept: ' + str(self._model.intercept_))
        print('MSE: ' + str(self._mse))
        print('R2 Score: ' + str(self._r2_score))

    def get_model_params(self):
        return '{' + '"model": "Linear regression", "coefficients": {coef}, "intercept": {intercept}, "MSE": {mse}, "RMSE": {rmse}, "r2_score": {r2_score}'.format(coef=self._model.coef_[0], intercept=self._model.intercept_, mse=self._mse, rmse=self._rmse, r2_score=self._r2_score) + '}'
