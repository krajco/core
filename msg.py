#!/usr/local/bin/python3.8
import socket

UDP_IP = "localhost"
UDP_PORT = 42333

MESSAGES = [
	'{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 100}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 90}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 80}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 70}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 60}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 50}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 40}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 30}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 20}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 10}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": 0}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -100}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -90}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -80}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -70}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -60}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -50}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -40}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -30}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -20}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -10}',
	# '{"object_id": "1.3.6.1.3.999.1.14.3.1", "friendly_name": "test", "seconds": 500, "timestamp": 15465465430, "day":2, "value": -0}',
]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
for MESSAGE in MESSAGES:
	sock.sendto(str.encode(MESSAGE), (UDP_IP, UDP_PORT))
	data, address = sock.recvfrom(4096)
	print(data)
