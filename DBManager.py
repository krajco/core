import psycopg2
import psycopg2.errors
import sys


class DBManager:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        try:
            self._connection = psycopg2.connect(database=db_name, user=user, password=password, host=host, port=port)
            self._cursor = self._connection.cursor()
            print('DB connection is estabilshed')
        except psycopg2.OperationalError as e:
            print('Connection error:' % e)

    def quit(self):
        self._cursor.close()
        self._connection.close()
        print('DB connection closed')

    def create_objects_table(self):
        table = 'iot_objects'

        drop_query = 'DROP TABLE IF EXISTS {table};'.format(table=table)
        self._cursor.execute(drop_query)
        self._connection.commit()

        create_objects_table = '''CREATE TABLE {table}
                            (OBJECT_ID TEXT NOT NULL,
                            FRIENDLY_NAME TEXT NOT NULL,
                            METHOD TEXT ,
                            UNIT TEXT ,
                            SENSOR_TYPE TEXT,
                            LEARNING_VALUES TEXT[],
                            DATE_FROM DATE,
                            PARAMS json,
                            PRIMARY KEY(OBJECT_ID));'''.format(table=table)
        self._cursor.execute(create_objects_table)
        self._connection.commit()
    #
    # def create_data_table(self):
    #     self._drop_table('iot_data')
    #     create_objects_table = '''CREATE TABLE iot_data
    #                         (INDEX BIGSERIAL,
    #                         OBJECT_ID TEXT NOT NULL,
    #                         TIMESTAMP INT NOT NULL,
    #                         SECONDS INT NOT NULL,
    #                         DAY_IN_WEEK INT NOT NULL,
    #                         VALUE REAL NOT NULL,
    #                         STATE INT NOT NULL,
    #                         PRIMARY KEY(INDEX));'''
    #     self._cursor.execute(create_objects_table)
    #     self._connection.commit()

    def update_model_params(self, model_params, object_id):
        query = 'UPDATE iot_objects SET PARAMS = \'{params}\' WHERE OBJECT_ID = \'{object_id}\';'.format(params=model_params, object_id=object_id)
        self._cursor.execute(query)
        self._connection.commit()

    def sensor_registration(self, object_id, friendly_name, method, type, date):
        register_query = 'INSERT INTO iot_objects (OBJECT_ID, FRIENDLY_NAME, METHOD, SENSOR_TYPE, DATE_FROM) VALUES (\'{object_id}\', \'{name}\', \'{method}\', \'{type}\',\'{date}\')'.format(object_id=object_id, name=friendly_name, method=method, type=type, date=date)
        self._cursor.execute(register_query)
        self._connection.commit()
        # print('Registration completed: ' + friendly_name, file=sys.stderr)

    # def sensor_exist(self, object_id):
    #     sensor_query = 'SELECT OBJECT_ID FROM iot_objects where OBJECT_ID = \'{object_id}\''.format(object_id=object_id)
    #     self._cursor.execute(sensor_query)
    #     return len(self._cursor.fetchall()) > 0

    # def insert_objects(self, object_id, friendly_name):
    #     insert_query = 'INSERT INTO iot_objects (OBJECT_ID, FRIENDLY_NAME) VALUES (\'{object_id}\', \'{name}\')'.format(object_id=object_id, name=friendly_name)
    #     self._cursor.execute(insert_query)
    #     self._connection.commit()

    def get_sensor_params(self, object_id):
        sensor_query = 'SELECT DATE_FROM FROM iot_objects where OBJECT_ID = \'{object_id}\''.format(object_id=object_id)
        self._cursor.execute(sensor_query)
        date = self._cursor.fetchone()[0]

        sensor_query = 'SELECT LEARNING_VALUES FROM iot_objects where OBJECT_ID = \'{object_id}\''.format(object_id=object_id)
        self._cursor.execute(sensor_query)
        cols = self._cursor.fetchone()[0]

        return date, cols

    def get_method(self, object_id):
        sensor_query = 'SELECT METHOD FROM iot_objects where OBJECT_ID = \'{object_id}\''.format(object_id=object_id)
        self._cursor.execute(sensor_query)
        return self._cursor.fetchone()[0]

    # def get_columns(self, object_id):
    #     sensor_query = 'SELECT LEARNING_VALUES FROM iot_objects where OBJECT_ID = \'{object_id}\''.format(object_id=object_id)
    #     self._cursor.execute(sensor_query)
    #     return self._cursor.fetchone()[0]

    def insert_data(self, object_id, timestamp, seconds, day, value, state):
        insert_query = 'INSERT INTO iot_data (OBJECT_ID, TIMESTAMP, SECONDS, DAY_IN_WEEK, VALUE, STATE) VALUES (\'{object_id}\', {timestamp}, {seconds}, {day}, {value}, {state})'.format(object_id=object_id, timestamp=timestamp, seconds=seconds, day=day, value=value, state=state)
        self._cursor.execute(insert_query)
        self._connection.commit()

    def _columns_to_str(self, columns):
        str_columns = ''
        for column in columns:
            str_columns += column + ','
        return str_columns[:-1]

    def get_train_data(self, object_id, columns, between=''):
        query = 'SELECT {cols} from iot_data WHERE OBJECT_ID = \'{oid}\' {between}'.format(cols=self._columns_to_str(columns), oid=object_id, between=between)
        self._cursor.execute(query)
        return self._cursor.fetchall()

    def update_cols(self, columns, object_id):
        query = 'UPDATE iot_objects SET LEARNING_VALUES = ARRAY[{cols}] WHERE OBJECT_ID = \'{object_id}\';'.format(cols=columns, object_id=object_id)
        self._cursor.execute(query)
        self._connection.commit()
