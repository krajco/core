import numpy as np
import LogManager
import pandas as pd
from enum import Enum
from datetime import datetime
from NagiosStates import NagiosState
import sys

from NormalDistributionClassifier import NormalDistributionClassifier
from PolynomialRegressionClassifier import PolynomialRegressionClassifier
from LinearRegressionClassifier import LinearRegressionClassifier
from IsolationForestClassifier import IsolationForestClassifier
from LocalOutliersFactorClassifier import LocalOutliersFactorClassifier


class Attributes(Enum):
    Date = 'Date'
    Day_in_week = 'Day in week'
    Day_in_year = 'Day in year'
    Time = 'Time'
    Value = 'Value'
    Seconds = 'Seconds'
    Timestamp = 'Timestamp'


class AttributesDB(Enum):
    Day_in_week = 'DAY_IN_WEEK'
    Value = 'VALUE'
    Seconds = 'SECONDS'
    Timestamp = 'TIMESTAMP'


def time_to_sec(time):
    h, m, s = map(int, time.split(':'))
    return h * 3600 + m * 60 + s

def get_model_name(model):
    if type(model) == PolynomialRegressionClassifier:
        return 'Polynomial regression'
    if type(model) == LinearRegressionClassifier:
        return 'Linear regression'
    if type(model) == IsolationForestClassifier:
        return 'Isolation forest'
    if type(model) == NormalDistributionClassifier:
        return 'Gausian method'
    if type(model) == LocalOutliersFactorClassifier:
        return 'Local outlier factor'


class Sensor:
    def __init__(self, object_id, friendly_name, model, db_manager, type='numeric', date_from='01-01-2022'):
        self._object_id = object_id
        self._friendly_name = friendly_name
        if model != None:
            self._model = model()
        else:
            self._model = None
        self._log_manager = LogManager.LogManager(object_id)
        self._merged_logfile = None
        self._value = None
        self._columns = []
        self._db_interval = ''
        self._db_manager = db_manager
        self._db_training = False
        self._type = type
        self._date_from = date_from
        # self._db_registration()

    def _db_registration(self):
        # if self._db_manager.sensor_exist(self._object_id) == False:
        self._db_manager.sensor_registration(self._object_id, self._friendly_name, get_model_name(self._model), self._type, self._date_from)
            # print('Sensor oid: {object_id} Friendly name: {friendly_name} registration completed!'.format(object_id=self._object_id, friendly_name=self._friendly_name), file=sys.stderr)

    def set_log_manager(self, date_from, date_to='12-31-2099'):
        self._log_manager.set_date(date_from, date_to)

    def set_logfile(self, filename):
        self._merged_logfile = filename

    def merge(self):
        self._log_manager.make_merge()

    def train(self, columns, data_type):
        if self._merged_logfile is None:
            self._merged_logfile = self._log_manager.merge_log_files()
        self._columns = columns
        df = pd.read_csv(self._merged_logfile, delimiter=',', dtype=data_type).loc[:, self._columns]
        self._model.fit(df.to_numpy())

        self._update_sensor_params()
        print(self._friendly_name + ' - Training completed', file=sys.stderr)

    def train_db(self):
        date, self._columns = self._db_manager.get_sensor_params(self._object_id)

        # date = self._db_manager.get_date(self._object_id)
        if date:
            self.set_db_interval(date)

        # self._columns = self._db_manager.get_columns(self._object_id)
        # print(self._columns)
        # print(type(self._columns))
        if self._columns:
            db_rows = self._db_manager.get_train_data(self._object_id, self._columns, self._db_interval)
            data = np.array(db_rows)
            self._model.fit(data)

        self._update_model_params()
        print(self._friendly_name + ' - Training completed - DB')

    def set_db_interval(self, date_from, date_to='2099-12-31'):
        start = int(date_from.strftime('%s'))
        end = int(datetime.strptime(date_to, '%Y-%m-%d').strftime('%s'))
        self._db_interval = 'AND timestamp BETWEEN {date_from} AND {date_to}'.format(date_from=start, date_to=end)

    def _update_model_from_db(self):
        model_db = self._db_manager.get_method(self._object_id)
        if model_db == 'Polynomial regression':
            self._model = PolynomialRegressionClassifier()
        if model_db == 'Linear regression':
            self._model = LinearRegressionClassifier()
        if model_db == 'Gausian method':
            self._model = NormalDistributionClassifier()
        if model_db == 'Isolation forest':
            self._model = IsolationForestClassifier()
            # self.set_param({"contamination": 0.01, "max_samples": 5000})

    def get_object_id(self):
        return self._object_id

    def get_sensor_state(self, value):
        self._value = value
        if self._model == None:
            self._db_training = True

        if self._db_training:
            self._update_model_from_db()
            if self._model:
                self.train_db()
                values = self._prepare_value_db()
                if self._model.predict(values):
                    return NagiosState.OK
        else:
            values = self._prepare_value()
            if self._model.predict(values):
                return NagiosState.OK
        return NagiosState.Warning
    #
    # def _prepare_value_db(self):
    #     values = []
    #     for attribute in self._columns:
    #         if attribute == AttributesDB.Day_in_week.value:
    #             values.append(datetime.today().weekday() + 1)
    #         if attribute == AttributesDB.Seconds.value:
    #             values.append(time_to_sec(datetime.now().time().strftime('%H:%M:%S')))
    #         if attribute == AttributesDB.Timestamp.value:
    #             values.append(datetime.now().timestamp())
    #         if attribute == AttributesDB.Value.value:
    #             values.append(self._value)
    #     return values

    def _prepare_value(self):
        values = []
        if self._db_training:
            for attribute in self._columns:
                if attribute == AttributesDB.Day_in_week.value:
                    values.append(datetime.today().weekday() + 1)
                if attribute == AttributesDB.Seconds.value:
                    values.append(time_to_sec(datetime.now().time().strftime('%H:%M:%S')))
                if attribute == AttributesDB.Timestamp.value:
                    values.append(datetime.now().timestamp())
                if attribute == AttributesDB.Value.value:
                    values.append(self._value)

        else:
            for attribute in self._columns:
                if attribute == Attributes.Date.value:
                    values.append(datetime.now().strftime('%m/%d/%y'))
                if attribute == Attributes.Day_in_week.value:
                    values.append(datetime.today().weekday() + 1)
                if attribute == Attributes.Day_in_year.value:
                    values.append(int(datetime.today().strftime('%j')))
                if attribute == Attributes.Time.value:
                    values.append(datetime.now().time().strftime('%H:%M:%S'))
                if attribute == Attributes.Seconds.value:
                    values.append(time_to_sec(datetime.now().time().strftime('%H:%M:%S')))
                if attribute == Attributes.Timestamp.value:
                    values.append(datetime.now().timestamp())
                if attribute == Attributes.Value.value:
                    values.append(self._value)
        return values

    def set_param(self, values):
        self._model.set_model(values)

    def _update_sensor_params(self):
        json_data = self._model.get_model_params()
        self._db_manager.update_model_params(json_data, self._object_id)

        columns = ''
        for col in self._columns:
            columns += '\'{col}\', '.format(col=col.replace(' ', '_'))
        columns = columns[:-2]
        # self._db_manager.update_cols(columns.upper(), self._object_id)

    # Testovacie prostredie
