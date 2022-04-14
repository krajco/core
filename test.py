#!/usr/local/bin/python3.8

import signal
import socket

from NagiosStates import NagiosState
from SensorState import SensorState
from Sensor import Sensor
from SensorManager import SensorManager
from MessageParser import MessageParser
from NormalDistributionClassifier import NormalDistributionClassifier
from PolynomialRegressionClassifier import PolynomialRegressionClassifier
from LinearRegressionClassifier import LinearRegressionClassifier
from DecisionTreeClassifier import DecisionTreeClassifier
from datetime import datetime
from DBManager import DBManager
from LogManager import time_to_sec

from enum import Enum


class ReadingData:
    def __init__(self):
        self._read = True

    def handler(self, signum, frame):
        self._read = False

    def read(self):
        return self._read


def make_registration(db_manager=None):
    manager = SensorManager()

    # Doors sensor initializing
    # door_c305 = Sensor('1.3.6.1.3.999.1.15.3.1', 'Door C305', DecisionTreeClassifier, db_manager)
    door_c306 = Sensor('1.3.6.1.3.999.1.15.3.2', 'Door C306', DecisionTreeClassifier, db_manager)
    # door_c307 = Sensor('1.3.6.1.3.999.1.15.3.3', 'Door C307', DecisionTreeClassifier, db_manager)
    # door_c308 = Sensor('1.3.6.1.3.999.1.15.3.4', 'Door C308', DecisionTreeClassifier, db_manager)
    #
    # door_c305.set_param({"contamination": 0.01, "max_samples": 50000})
    # door_c306.set_param({"contamination": 0.01, "max_samples": 50000})
    # door_c307.set_param({"contamination": 0.01, "max_samples": 50000})
    # door_c308.set_param({"contamination": 0.01, "max_samples": 50000})
    #
    # door_c305.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    door_c306.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # door_c307.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # door_c308.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    #
    # manager.register(door_c305)
    manager.register(door_c306)
    # manager.register(door_c307)
    # manager.register(door_c308)
    #
    # # Windows sensor initializing
    # window_c306 = Sensor('1.3.6.1.3.999.1.15.3.6', 'Window C306', DecisionTreeClassifier, db_manager)
    # window_c307 = Sensor('1.3.6.1.3.999.1.15.3.7', 'Window C307', DecisionTreeClassifier, db_manager)
    # window_c308_left = Sensor('1.3.6.1.3.999.1.15.3.5', 'Window C308 left', DecisionTreeClassifier, db_manager)
    #
    # window_c306.set_param({"contamination": 0.01, "max_samples": 5000})
    # window_c307.set_param({"contamination": 0.01, "max_samples": 5000})
    # window_c308_left.set_param({"contamination": 0.01, "max_samples": 5000})
    #
    # window_c306.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # window_c307.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # window_c308_left.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    #
    # manager.register(window_c306)
    # manager.register(window_c307)
    # manager.register(window_c308_left)
    #
    # # ESP32 Cameras temperature initializing
    # esp32_cam01_temp = Sensor('1.3.6.1.3.999.1.12.3.1', 'ESP32 Cam01 temperature', NormalDistributionClassifier, db_manager)
    # esp32_cam02_temp = Sensor('1.3.6.1.3.999.1.12.3.2', 'ESP32 Cam02 temperature', NormalDistributionClassifier, db_manager)
    # esp32_cam03_temp = Sensor('1.3.6.1.3.999.1.12.3.3', 'ESP32 Cam03 temperature', NormalDistributionClassifier, db_manager)
    # esp32_cam04_temp = Sensor('1.3.6.1.3.999.1.12.3.4', 'ESP32 Cam04 temperature', NormalDistributionClassifier, db_manager)
    #
    # esp32_cam01_temp.train(['Value'], {'Value': float})
    # esp32_cam02_temp.train(['Value'], {'Value': float})
    # esp32_cam03_temp.train(['Value'], {'Value': float})
    # esp32_cam04_temp.train(['Value'], {'Value': float})

    # manager.register(esp32_cam01_temp)
    # manager.register(esp32_cam02_temp)
    # manager.register(esp32_cam03_temp)
    # manager.register(esp32_cam04_temp)
    #
    # # ESP32 Cameras signal initializing
    # esp32_cam01_signal = Sensor('1.3.6.1.3.999.1.14.3.1', 'ESP32 Cam01 RSSI', NormalDistributionClassifier, db_manager)
    # esp32_cam02_signal = Sensor('1.3.6.1.3.999.1.14.3.2', 'ESP32 Cam02 RSSI', PolynomialRegressionClassifier, db_manager)
    # esp32_cam03_signal = Sensor('1.3.6.1.3.999.1.14.3.3', 'ESP32 Cam03 RSSI', PolynomialRegressionClassifier, db_manager)
    # esp32_cam04_signal = Sensor('1.3.6.1.3.999.1.14.3.4', 'ESP32 Cam04 RSSI', PolynomialRegressionClassifier, db_manager)
    #
    # esp32_cam01_signal.set_log_manager('01-01-2022')
    # esp32_cam02_signal.set_log_manager('01-01-2022')
    # esp32_cam03_signal.set_log_manager('01-01-2022')
    # esp32_cam04_signal.set_log_manager('01-01-2022')
    #
    # esp32_cam01_signal.train(['Value'], {'Value': float})
    # esp32_cam02_signal.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # esp32_cam03_signal.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # esp32_cam04_signal.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    #
    # esp32_cam01_signal.update_model_params()
    # manager.register(esp32_cam01_signal)
    # manager.register(esp32_cam02_signal)
    # manager.register(esp32_cam03_signal)
    # manager.register(esp32_cam04_signal)
    #
    # # Binary sensors battery
    # door_c305_battery = Sensor('1.3.6.1.3.999.1.17.3.1', 'Battery door C356', LinearRegressionClassifier, db_manager)
    # door_c306_battery = Sensor('1.3.6.1.3.999.1.17.3.2', 'Battery door C306', LinearRegressionClassifier, db_manager)
    # door_c308_battery = Sensor('1.3.6.1.3.999.1.17.3.4', 'Battery door C308', LinearRegressionClassifier, db_manager)
    # window_battery_c308_left = Sensor('1.3.6.1.3.999.1.17.3.5', 'Battery window C308 left', LinearRegressionClassifier, db_manager)
    # window_battery_c306 = Sensor('1.3.6.1.3.999.1.17.3.6', 'Battery window C306', LinearRegressionClassifier, db_manager)
    # window_battery_c307 = Sensor('1.3.6.1.3.999.1.17.3.7', 'Battery window C307', LinearRegressionClassifier, db_manager)
    # motion_battery_c306_right = Sensor('1.3.6.1.3.999.1.17.3.8', 'Battery motion C306 right', LinearRegressionClassifier, db_manager)
    # motion_battery_c307 = Sensor('1.3.6.1.3.999.1.17.3.9', 'Battery motion C307', LinearRegressionClassifier, db_manager)
    # motion_battery_c308_right = Sensor('1.3.6.1.3.999.1.17.3.10', 'Battery motion C308 right', LinearRegressionClassifier, db_manager)
    # motion_battery_c308_left = Sensor('1.3.6.1.3.999.1.17.3.11', 'Battery motion C308 left', LinearRegressionClassifier, db_manager)
    #
    # door_c305_battery.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # door_c306_battery.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # door_c308_battery.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # window_battery_c308_left.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # window_battery_c306.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # window_battery_c307.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # motion_battery_c306_right.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # motion_battery_c307.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # motion_battery_c308_right.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    # motion_battery_c308_left.train(['Timestamp', 'Value'], {'Timestamp': int, 'Value': float})
    #
    # manager.register(door_c305_battery)
    # manager.register(door_c306_battery)
    # manager.register(door_c308_battery)
    # manager.register(window_battery_c308_left)
    # manager.register(window_battery_c306)
    # manager.register(window_battery_c307)
    # manager.register(motion_battery_c306_right)
    # manager.register(motion_battery_c307)
    # manager.register(motion_battery_c308_right)
    # manager.register(motion_battery_c308_left)
    #
    # # Motions sensors state
    # motion_c306_right = Sensor('1.3.6.1.3.999.1.16.3.1', 'Motion C306 right', DecisionTreeClassifier, db_manager)
    # motion_c306_left = Sensor('1.3.6.1.3.999.1.16.3.2', 'Motion C306 left', DecisionTreeClassifier, db_manager)
    # motion_c307 = Sensor('1.3.6.1.3.999.1.16.3.3', 'Motion C307', DecisionTreeClassifier, db_manager)
    # motion_c308_left = Sensor('1.3.6.1.3.999.1.16.3.4', 'Motion C308 left', DecisionTreeClassifier, db_manager)
    # motion_c308_right = Sensor('1.3.6.1.3.999.1.16.3.5', 'Motion C308 right', DecisionTreeClassifier, db_manager)
    #
    # motion_c306_right.set_param({"contamination": 0.01, "max_samples": 5000})
    # motion_c306_left.set_param({"contamination": 0.01, "max_samples": 5000})
    # motion_c307.set_param({"contamination": 0.01, "max_samples": 5000})
    # motion_c308_left.set_param({"contamination": 0.01, "max_samples": 5000})
    # motion_c308_right.set_param({"contamination": 0.01, "max_samples": 5000})
    #
    # motion_c306_right.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # motion_c306_left.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # motion_c307.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # motion_c308_left.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    # motion_c308_right.train(['Day in week', 'Seconds', 'Value'], {'Day in week': int, 'Seconds': int, 'Value': int})
    #
    # manager.register(motion_c306_right)
    # manager.register(motion_c306_left)
    # manager.register(motion_c307)
    # manager.register(motion_c308_left)
    # manager.register(motion_c308_right)
    #
    # shp6_fridge_today = Sensor('1.3.6.1.3.999.1.7.3.9', 'SHP6 fridge today', LinearRegressionClassifier, db_manager)
    # shp6_pc_letavay_today = Sensor('1.3.6.1.3.999.1.7.3.11', 'SHP6 PC Letavay today', LinearRegressionClassifier, db_manager)
    # shp6_pc_koutensky_today = Sensor('1.3.6.1.3.999.1.7.3.13', 'SHP6 PC Koutensky today', LinearRegressionClassifier, db_manager)
    # shp6_pc_vecera_today = Sensor('1.3.6.1.3.999.1.7.3.14', 'SHP6 PC Vecera today', LinearRegressionClassifier, db_manager)
    #
    # shp6_fridge_today.train(['Seconds', 'Value'], {'Seconds': int, 'Value': float})
    # shp6_pc_letavay_today.train(['Seconds', 'Value'], {'Seconds': int, 'Value': float})
    # shp6_pc_koutensky_today.train(['Seconds', 'Value'], {'Seconds': int, 'Value': float})
    # shp6_pc_vecera_today.train(['Seconds', 'Value'], {'Seconds': int, 'Value': float})
    #
    # manager.register(shp6_fridge_today)
    # manager.register(shp6_pc_letavay_today)
    # manager.register(shp6_pc_koutensky_today)
    # manager.register(shp6_pc_vecera_today)
    #
    # shp6_fridge_total = Sensor('1.3.6.1.3.999.1.5.3.9', 'SHP6 fridge total', LinearRegressionClassifier, db_manager)
    # shp6_pc_letavay_total = Sensor('1.3.6.1.3.999.1.5.3.11', 'SHP6 PC Letavay total', LinearRegressionClassifier, db_manager)
    # shp6_pc_koutensky_total = Sensor('1.3.6.1.3.999.1.5.3.13', 'SHP6 PC Koutensky total', LinearRegressionClassifier, db_manager)
    # shp6_pc_vecera_total = Sensor('1.3.6.1.3.999.1.5.3.14', 'SHP6 PC Vecera total', LinearRegressionClassifier, db_manager)
    #
    # shp6_fridge_total.train(['Timestamp', 'Value'], {'Seconds': int, 'Value': float})
    # shp6_pc_letavay_total.train(['Timestamp', 'Value'], {'Seconds': int, 'Value': float})
    # shp6_pc_koutensky_total.train(['Timestamp', 'Value'], {'Seconds': int, 'Value': float})
    # shp6_pc_vecera_total.train(['Timestamp', 'Value'], {'Seconds': int, 'Value': float})

    # manager.register(shp6_fridge_total)
    # manager.register(shp6_pc_letavay_total)
    # manager.register(shp6_pc_koutensky_total)
    # manager.register(shp6_pc_vecera_total)
    #
    # shp6_fridge_voltage = Sensor('1.3.6.1.3.999.1.10.3.9', 'SHP6 fridge voltage', NormalDistributionClassifier, db_manager)
    # shp6_pc_letavay_voltage = Sensor('1.3.6.1.3.999.1.10.3.11', 'SHP6 PC Letavay voltage', NormalDistributionClassifier, db_manager)
    # shp6_pc_koutensky_voltage = Sensor('1.3.6.1.3.999.1.10.3.13', 'SHP6 PC Koutensky voltage', NormalDistributionClassifier, db_manager)
    # shp6_pc_vecera_voltage = Sensor('1.3.6.1.3.999.1.10.3.14', 'SHP6 PC Vecera voltage', NormalDistributionClassifier, db_manager)
    #
    # shp6_fridge_voltage.train(['Value'], {'Value': float})
    # shp6_pc_letavay_voltage.train(['Value'], {'Value': float})
    # shp6_pc_koutensky_voltage.train(['Value'], {'Value': float})
    # shp6_pc_vecera_voltage.train(['Value'], {'Value': float})
    #
    # manager.register(shp6_fridge_voltage)
    # manager.register(shp6_pc_letavay_voltage)
    # manager.register(shp6_pc_koutensky_voltage)
    # manager.register(shp6_pc_vecera_voltage)

    return manager


if __name__ == '__main__':
    # Variables
    # message_parser = MessageParser()

    # Core configurations
    # local_ip = '127.0.0.1'
    # local_port = 42333
    # buffer_size = 1024
    # # DB manager initializing
    # db_manager = DBManager('core_db', 'core', 'motorhead', '2001:67c:1220:809:20c:29ff:fee9:cbd3')
    # db_manager.create_objects_table()
    # db_manager.create_data_table()

    # server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    # server_socket.bind((local_ip, local_port))
    # print('Server listening: ' + local_ip + '/' + str(local_port))
    # sensor_manager = make_registration(db_manager)
    #
    # reader = ReadingData()
    # signal.signal(signal.SIGINT, reader.handler)
    test = PolynomialRegressionClassifier()
    print(type(test))
    if type(test) == NormalDistributionClassifier:
        print('Yees')


    # print('Learning completed!')
    # while reader.read():
    #     message, address = server_socket.recvfrom(buffer_size)
    #     state = NagiosState.OK
    #     if message_parser.set_message(message):
    #         timestamp = int(datetime.now().timestamp())
    #         seconds = time_to_sec(datetime.now().time().strftime("%H:%M:%S"))
    #         day = datetime.now().strftime('%w')
    #
    #         if sensor_manager.is_registered(message_parser.get_object_id()) == SensorState.Registered:
    #             state = sensor_manager.get_state(message_parser.get_value())
    #         # else:
    #             # new_sensor = Sensor(message_parser.get_object_id(), message_parser.get_service(), None, db_manager)
    #             # sensor_manager.register(new_sensor)
    #         db_manager.insert_data(message_parser.get_object_id(), timestamp, seconds, day, message_parser.get_value(), state.value)
    #
    #     server_socket.sendto(str.encode(str(state.value)), address)

    # db_manager.quit()
#
