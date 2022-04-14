import json
import sys


class MessageParser:
    def __init__(self):
        self._msg = None

    def set_message(self, message):
        try:
            self._msg = json.loads(message.decode('utf8').replace("'", '"').replace('\\n', ''))
            return True
        except ValueError as e:
            print('Incorrect message format, invalid JSON', file=sys.stderr)
            print(message)
            print(e, file=sys.stderr)
            return False

    def get_object_id(self):
        return self._msg['object_id']

    def get_service(self):
        return self._msg['service']

    def get_value(self):
        return self._msg['value']

    def get_timestamp(self):
        return self._msg['timestamp']

    def get_day(self):
        return self._msg['day']

    def get_seconds(self):
        return self._msg['seconds']

    def is_test(self):
        if 'seconds' in self._msg:
            return True
        return False
