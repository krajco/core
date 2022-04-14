#!/usr/local/bin/python3.8
import psycopg2
import psycopg2.errors
from os import walk
from datetime import datetime


def time_to_sec(t):
    h, m, s = map(int, t.split(':'))
    return h * 3600 + m * 60 + s


def is_float(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


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

    def _drop_table(self, table):
        table = 'DROP TABLE IF EXISTS {table};'.format(table=table)
        self._cursor.execute(table)
        self._connection.commit()

    def create_objects_table(self):
        self._drop_table('iot_test')
        create_objects_table = '''CREATE TABLE iot_test
                            (OBJECT_ID TEXT NOT NULL,
                            FRIENDLY_NAME TEXT NOT NULL,
                            LEARNING_VALUES TEXT[],
                            DATE_FROM DATE,
                            PRIMARY KEY(OBJECT_ID));'''
        self._cursor.execute(create_objects_table)
        self._connection.commit()

    def create_data_table(self):
        self._drop_table('iot_data')
        create_objects_table = '''CREATE TABLE iot_data
                            (INDEX BIGSERIAL,
                            OBJECT_ID TEXT NOT NULL,
                            TIMESTAMP INT NOT NULL,
                            SECONDS INT NOT NULL,
                            DAY_IN_WEEK INT NOT NULL,
                            VALUE REAL NOT NULL,
                            STATE INT NOT NULL,
                            PRIMARY KEY(INDEX));'''
        self._cursor.execute(create_objects_table)
        self._connection.commit()

    def insert_objects(self, object_id, friendly_name):
        insert_query = 'INSERT INTO iot_objects (OBJECT_ID, FRIENDLY_NAME) VALUES (\'{object_id}\', \'{name}\')'.format(object_id=object_id, name=friendly_name)
        self._cursor.execute(insert_query)
        self._connection.commit()

    def insert_data(self, object_id, timestamp, seconds, day, value, state):
        insert_query = 'INSERT INTO iot_data (OBJECT_ID, TIMESTAMP, SECONDS, DAY_IN_WEEK, VALUE, STATE) VALUES (\'{object_id}\', {timestamp}, {seconds}, {day}, {value}, {state})'.format(object_id=object_id, timestamp=timestamp, seconds=seconds, day=day, value=value, state=state)
        self._cursor.execute(insert_query)
        self._connection.commit()

    def get_data_table(self):
        table_rows = 'SELECT * FROM iot_data;'
        self._cursor.execute(table_rows)
        return self._cursor.fetchall()


    def select(self, str):
        self._cursor.execute(str)
        return self._cursor.fetchall()


    def update(self, str):
        self._cursor.execute(str)
        self._connection.commit()

# def update_objects_table():

def update_data_table(db_manager) :
    db_manager.create_data_table()
    dir_path = '/var/log/nagios/'
    log_dates = next(walk(dir_path), (None, None, []))[1]
    all_log_files = []

    for log_date in log_dates:
        log_dir_path = dir_path + log_date
        log_files = next(walk(log_dir_path), (None, None, []))
        all_log_files.append(log_files)

    cnt = 0
    for log_path, _, log_files in all_log_files:
        for log_file in log_files:
            oid = log_file.replace('.log', '')
            file = '{dir}/{file}'.format(dir=log_path, file=log_file)
            data = open(file, 'r').read().split('\n')

            for item in data:
                cells = item.split(' ')
                if len(cells) > 2 and cells[2].split('/')[0] != 'unavailable':
                    date = cells[0].replace('[', '')
                    date_indexes = date.split('/')

                    value = cells[2].split('/')[0]
                    if is_float(value):
                        day_index = datetime(int(date_indexes[2]), int(date_indexes[0]), int(date_indexes[1]))
                        time = cells[1].replace(']', '')
                        timestamp_time_in_day = time_to_sec(time)
                        timestamp_datetime = datetime.strptime(date, "%m/%d/%y").timestamp() + timestamp_time_in_day
                        day_in_week = day_index.strftime('%w')
                        day_in_year = day_index.strftime('%j')
                        db_manager.insert_data(oid, timestamp_datetime, timestamp_time_in_day, day_in_week, value, 0)
                        cnt += 1

db_manager = DBManager('core_db', 'core', 'motorhead', '2001:67c:1220:809:20c:29ff:fee9:cbd3')
update_data_table(db_manager)
# db_manager.create_data_table()
#
# # str = 'SELECT (STATE) FROM iot_data WHERE OBJECT_ID = \'1.3.6.1.3.999.1.15.3.3\' ORDER BY INDEX LIMIT 1;'
# # str = 'SELECT COUNT(STATE), SUM(STATE) FROM iot_data  where OBJECT_ID = \'1.3.6.1.3.999.1.15.3.3\';'
# str = 'INSERT INTO iot_test VALUES(\'1.3.6.1.3.999.1.15.3.1\', \'test\', ARRAY[\'seconds\', \'value\'],\'1980-01-01\');'
# db_manager.update(str)
#
#str = 'UPDATE iot_objects SET FRIENDLY_NAME = \'ESP32 Cam01 temperature\', METHOD =\'Gausian method\', SENSOR_TYPE =\'numeric\', UNIT = \'\', LEARNING_VALUES = ARRAY[\'\'] WHERE OBJECT_ID = \'1.3.6.1.3.999.1.12.3.1\';'
# str = 'UPDATE iot_objects SET FRIENDLY_NAME = \'ESP32 Cam01 temperature\', METHOD =\'Gausian method\', SENSOR_TYPE =\'numeric\', UNIT = \'\', LEARNING_VALUES = ARRAY[\'VALUE\'] WHERE OBJECT_ID = \'1.3.6.1.3.999.1.12.3.1\';'
# db_manager.update(str)
#
# str = 'Select * from iot_objects ORDER BY OBJECT_ID ASC LIMIT 1;'
# rows = db_manager.select(str)
# for row in rows:
#     print(row)


# rows = db_manager.get_data_table()
# print(cnt)
# print(len(rows))
# "UPDATE iot_objects SET FRIENDLY_NAME = '$arr[1]', METHOD ='$arr[2]', SENSOR_TYPE ='$arr[3]', UNIT = '$arr[4]' WHERE OBJECT_ID = '$arr[0]';";

# data = [['1.3.6.1.3.999.1.7.3.9', 'SHP6 fridge today', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.7.3.14', 'SHP6 PC Vecera today', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.7.3.13', 'SHP6 PC Koutensky today', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.7.3.11', 'SHP6 PC Letavay today', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.5.3.9', 'SHP6 fridge total', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.5.3.14', 'SHP6 PC Vecera total', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.5.3.13', 'SHP6 PC Koutensky total', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.5.3.11', 'SHP6 PC Letavay total', 'Linear regression', 'kWh', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.9', 'Battery motion C307', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.8', 'Battery motion C306 right', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.7', 'Battery window C307', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.6', 'Battery window C306', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.5', 'Battery window C308 left', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.4', 'Battery door C308', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.2', 'Battery door C306', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.11', 'Battery motion C308 left', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.10', 'Battery motion C308 right', 'Polynomial regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.17.3.1', 'Battery door C356', 'Linear regression', '%', 'numeric'],
# ['1.3.6.1.3.999.1.16.3.5', 'Motion C308 right', 'Isolation forest', '', 'motion'],
# ['1.3.6.1.3.999.1.16.3.4', 'Motion C308 left', 'Isolation forest', '', 'motion'],
# ['1.3.6.1.3.999.1.16.3.3', 'Motion C307', 'Isolation forest', '', 'motion'],
# ['1.3.6.1.3.999.1.16.3.2', 'Motion C306 left', 'Isolation forest', '', 'motion'],
# ['1.3.6.1.3.999.1.16.3.1', 'Motion C306 right', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.7', 'Window C307', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.6', 'Window C306', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.5', 'Window C308 left', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.4', 'Door C308', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.3', 'Door C307', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.2', 'Door C306', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.15.3.1', 'Door C305', 'Isolation forest', '', 'magnetic'],
# ['1.3.6.1.3.999.1.14.3.4', 'ESP32 Cam04 RSSI', 'Polynomial regression', 'dBm', 'numeric'],
# ['1.3.6.1.3.999.1.14.3.3', 'ESP32 Cam03 RSSI', 'Polynomial regression', 'dBm', 'numeric'],
# ['1.3.6.1.3.999.1.14.3.2', 'ESP32 Cam02 RSSI', 'Polynomial regression', 'dBm', 'numeric'],
# ['1.3.6.1.3.999.1.14.3.1', 'ESP32 Cam01 RSSI', 'Polynomial regression', 'dBm', 'numeric'],
# ['1.3.6.1.3.999.1.12.3.4', 'ESP32 Cam04 temperature', 'Gausian method', '°C', 'numeric'],
# ['1.3.6.1.3.999.1.12.3.3', 'ESP32 Cam03 temperature', 'Gausian method', '°C', 'numeric'],
# ['1.3.6.1.3.999.1.12.3.2', 'ESP32 Cam02 temperature', 'Gausian method', '°C', 'numeric'],
# ['1.3.6.1.3.999.1.12.3.1', 'ESP32 Cam01 temperature', 'Gausian method', '°C', 'numeric'],
# ['1.3.6.1.3.999.1.10.3.9', 'SHP6 fridge voltage', 'Gausian method', 'V', 'numeric'],
# ['1.3.6.1.3.999.1.10.3.14', 'SHP6 PC Vecera voltage', 'Gausian method', 'V', 'numeric'],
# ['1.3.6.1.3.999.1.10.3.13', 'SHP6 PC Koutensky voltage', 'Gausian method', 'V', 'numeric'],
# ['1.3.6.1.3.999.1.10.3.11', 'SHP6 PC Letavay voltage', 'Gausian method', 'V', 'numeric']]
#
# # "UPDATE iot_objects SET FRIENDLY_NAME = '$arr[1]', METHOD ='$arr[2]', SENSOR_TYPE ='$arr[3]', UNIT = '$arr[4]' WHERE OBJECT_ID = '$arr[0]';";
# for row in data:
#     str = 'UPDATE iot_objects SET METHOD = \'{method}\', SENSOR_TYPE = \'{type}\', UNIT = \'{unit}\' WHERE OBJECT_ID = \'{oid}\';'.format(method=row[2], type=row[4], unit=row[3], oid=row[0])
#     # str = 'UPDATE iot_objects SET DATE_FROM = \'2022-01-01\' WHERE OBJECT_ID = \'{oid}\';'.format(method=row[2], type=row[4], unit=row[3], oid=row[0])
#     db_manager.update(str)
#     print(str)
# # str = 'UPDATE iot_objects SET DATE_FROM = \'2022-03-15\'WHERE OBJECT_ID = \'1.3.6.1.3.999.1.12.3.1\';'
# db_manager.update(str);
# db_manager.quit()
