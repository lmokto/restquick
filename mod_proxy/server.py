#!/usr/bin/env python
# -*- coding: utf-8 -*-

from getDistances import getDistance, load
import json
import zmq
import time

def main(estaciones):

	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:5555")

	while True:

		#  Wait for next request from client
		mi_ubicacion = socket.recv()

		# tengo lat+long
		print("Received request: %s" % mi_ubicacion)
		message = mi_ubicacion.split("::")

		distancias = getDistance({"lat": float(message[0]),"lng": float(message[1])}, estaciones)
		distancias.sort()

		#  Send reply back to client
		socket.send(json.dumps(distancias[0:5]))

		#
		time.sleep(1)

if __name__ == '__main__':

	with open("") as estaciones_bicis:
		estaciones_buffer = buffer(estaciones_bicis.read())
		estaciones = json.loads(estaciones_buffer.__str__())
	
	main(estaciones)