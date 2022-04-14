from datetime import datetime
from NagiosStates import NagiosState
from SensorState import SensorState


class SensorManager:
    def __init__(self):
        self._list = []
        self._active_sensor = {}

    def get_sensors(self):
        return self._list;

    def register(self, sensor):
        self._list.append(sensor)

    def is_registered(self, object_id):
        self._active_sensor = None
        for sensor in self._list:
            if sensor.get_object_id() == object_id:
                self._active_sensor = sensor
                return SensorState.Registered
        return SensorState.Unknown

    def get_state(self, value):
        return self._active_sensor.get_sensor_state(value)

    # Testovacia funkcia
    def get_test_value(timestamp, day, seconds, value):
        return self._active_sensor.get_test_sensor_state(value)
