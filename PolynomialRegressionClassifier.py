import matplotlib.pyplot as plt
import numpy as np

from math import sqrt
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from ClassifierAbstract import ClassifierAbstract


def plot_data(data, data_x, data_y, predicted):
    x = data_x.reshape(-1)
    y = data_y
    y.astype(float)

    index = 5
    date = [str(datetime.fromtimestamp(elem)) for elem in x]
    xx = [datetime.strptime(elem, '%Y-%m-%d %H:%M:%S') for elem in date]
    plt.scatter(xx[::index], y[::index])
    plt.plot(xx[::index], predicted[::index], color='red')
    plt.xticks(rotation=45)
    plt.ylabel('Signal [dBm]')
    plt.xlabel('Date')
    plt.ylim(0, 1)
    plt.show()


class PolynomialRegressionClassifier(ClassifierAbstract):
    def __init__(self):
        self._model = LinearRegression()
        self._mse = self._rmse = self._r2_score = self._standard_deviation = None
        self._degree = 1

    def fit(self, data):
        data_x = data[:, 0].reshape(-1, 1)
        data_y = data[:, 1]

        data_x = data_x[::10]
        data_y = data_y[::10]

        data_x_train, data_x_test, data_y_train, data_y_test = train_test_split(data_x, data_y, test_size=0.33)

        best_score = 0.0
        best_model = None
        for degree in range(2, 32):
            poly_reg = PolynomialFeatures(degree=degree)
            x_poly_train = poly_reg.fit_transform(data_x_train)
            poly_reg = LinearRegression()
            poly_reg.fit(x_poly_train, data_y_train)

            x_poly_test = PolynomialFeatures(degree=degree).fit_transform(data_x_test)
            data_y_predict = poly_reg.predict(x_poly_test)
            score = r2_score(data_y_test, data_y_predict)
            if best_score < score:
                best_model = poly_reg
                best_score = score
                self._degree = degree

        self._model = best_model
        self._r2_score = best_score

        x_poly_test = PolynomialFeatures(degree=self._degree).fit_transform(data_x_test)
        data_y_predict = self._model.predict(x_poly_test)

        self._mse = mean_squared_error(data_y_test, data_y_predict)
        self._rmse = mean_squared_error(data_y_test, data_y_predict, squared=False)
        self._standard_deviation = sqrt(self._mse)
#        result = self._model.predict(PolynomialFeatures(degree=self._degree).fit_transform(data_x.reshape(-1, 1)))
#        plot_data(data, data_x, data_y, result)
#        self.print_stats()

    def predict(self, value):
        value = np.array(value)
        x = PolynomialFeatures(degree=self._degree).fit_transform(value[0].reshape(-1, 1))
        y = value[1]
        err = abs(y - self._model.predict(x)[0])
        return err < 3 * self._standard_deviation

    def print_stats(self):
        print('Degree: ' + str(self._degree))
        print('Coefficients: ' + str(self._model.coef_[0]))
        print('Intercept: ' + str(self._model.intercept_))
        print('MSE: ' + str(self._mse))
        print('R2 Score: ' + str(self._r2_score))

    def get_model_params(self):
        coefs = ''
        for coef in self._model.coef_:
            coefs += str(coef) + ','
        coefs = coefs[:-1]

        return '{' + '"model": "Polynomial regression", "degree": {degree}, "coefficients": [{coef}], "intercept": {intercept}, "MSE": {mse}, "RMSE": {rmse}, "r2_score": {r2_score}'.format(degree=self._degree, coef=coefs, intercept=self._model.intercept_, mse=self._mse, rmse=self._rmse, r2_score=self._r2_score) + '}'
