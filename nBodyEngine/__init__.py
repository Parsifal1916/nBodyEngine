from . import Body
from . import GraphEngine
import json
import os

print('Modulo importato con successo')

def simulateFromJson(jsonFile: str) -> None:
	with open(jsonFile, 'r') as file:
		content = json.load(file) # estrae il contenuto del file

		#crea i corpi
		bodies: list = []
		_bodies: list = content['Bodies']
		for i in _bodies:
			try: useAccurateSize = content['Simulation']['useAccurateSize']
			except KeyError: useAccurateSize = False
			bodies.append(Body.Body(i, bodies, useAccurateSize = useAccurateSize))


		#comincia la simulazione
		simulation = GraphEngine.Graph(bodies, content['Simulation']['size'], content['Simulation']['graphs'])
		simulation.start(content['Simulation']['speed'])
