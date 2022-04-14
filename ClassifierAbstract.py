from abc import abstractmethod


class ClassifierAbstract:
    @abstractmethod
    def predict(self, value):
        raise NotImplementedError('Function must be implemented')

    @abstractmethod
    def fit(self, data):
        raise NotImplementedError('Function must be implemented')

    @abstractmethod
    def get_model_params(self):
        raise NotImplementedError('Function must be implemented')
