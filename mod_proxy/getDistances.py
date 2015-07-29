#!/usr/bin/env python
# -*- coding: utf-8 -*-

from math import sin, cos, sqrt, atan2, radians
import json

# approximate radius of earth in km
# http://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude-python#19412565

"""
	ejecutar este modulo en un processo, que este en modo server de 0MQ, REP

	necesito una funcion donde, le paso un json con lat+long y mi ubicacion, y me diga caules son las n cercanas

	lat1 = radians(-34.595584)
	lon1 = radians(-58.387229)

	lat2 = radians(-34.595443)
	lon2 = radians(-58.382851)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c

	print("Result:", distance)

	"tengo una lista completa de waypoint y tengo que pasarla a un array dentro de la clase
	para que cada lat+long sea un radians, entonces necesito una funcion que se ocupe de cargar todo

	with open('') as f:
		lolo = json.loads(f.read())
"""

mi_ubicacion = {
	"lat": -34.595584,
	"lng": -58.387229
}

def load(filename):

	with open(filename) as f:
		output = json.loads(f.read())

	return output

def getDistance(ubi={}, waypoints={}):

	R = 6373.0
	my_lat = radians(ubi["lat"])
	my_lng = radians(ubi["lng"])
	results = []
	
	for points in waypoints:
		#points.pop('id')
		for key, value in points.iteritems():
			#print key, value
			if key == "latitude":
				lat = radians(value)
				dlat = my_lat - lat

			if key == "longitude":
				lng = radians(value)
				dlon = my_lng - lng
		
		a = sin(dlat / 2)**2 + cos(my_lat) * cos(lat) * sin(dlon / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		distance = R * c
		points.update({'distancia': distance})
		results.append(points)

	return results


def main():

	estaciones = load("")
	distancias = getDistance(mi_ubicacion, estaciones)
	distancias.sort()
	print distancias[0:5]


if __name__ == '__main__':
	main()