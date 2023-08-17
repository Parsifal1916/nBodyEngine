from . import Body
from . import GraphEngine
import json
import os

print('nBodyEngine Installed Successfully!')


def simulateFromJson(jsonFile: str) -> None:
	print('loading json file...')
	with open(jsonFile, 'r') as file:
		content = json.load(file) # estrae il contenuto del file

		simulation=GraphEngine.Graph(
			[], 
			content['Simulation']['size'], 
			content['Simulation']['graphs'], 
			toggleInstableOrbits = content['Simulation'].get('toggleInstableOrbits', False),
			dimensions = content['Simulation'].get('style', 2)
		)

		bodies: list = []
		_bodies: list = content['Bodies']

		#crea i corpi basandosi sul file json
		for i in _bodies:
			try: useAccurateSize = content['Simulation']['useAccurateSize']
			except KeyError: useAccurateSize = False
			bodies.append(Body.Body(
				i, 
				simulation, 
				useAccurateSize = content['Simulation'].get('useAccurateSize', False),
				includeSR = content['Simulation'].get('includeSR', False),
				dimensions = content['Simulation'].get('style', 2)
				))

		simulation.bodies = bodies

		#comincia la simulazione
		print('starting the simulation..')
		simulation.start(content['Simulation']['speed'])
