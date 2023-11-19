from . import Body
from . import GraphEngine
import json
import os

print('nBodyEngine Installed Successfully!')

def simulateFromJson(jsonFile: str) -> None:
	print('loading json file...')
	with open(jsonFile, 'r') as file:
		content = json.load(file) # estrae il contenuto del file

		#comincia la simulazione
		simulation=GraphEngine.Graph(
			content['Simulation']['size'], 
			graphs = content['Simulation']['graphs'], 
			toggleInstableOrbits = content['Simulation'].get('toggleInstableOrbits', False),
			pathTracing = content['Simulation'].get('pathTracing', False),
			dimensions = content['Simulation'].get('style', 2)
		)

		#crea i corpi
		bodies: list = []
		_bodies: list = content['Bodies']
		for i in _bodies:
			try: useAccurateSize = content['Simulation']['useAccurateSize']
			except KeyError: useAccurateSize = False
			bodies.append(Body.Body(
				simulation,
				i, 
				useAccurateSize = content['Simulation'].get('useAccurateSize', False),
				includeSR = content['Simulation'].get('includeSR', False),
				dimensions = content['Simulation'].get('style', 2)
				))

		del _bodies
		simulation.bodies = bodies

		print('starting the simulation..')
		simulation.start(content['Simulation']['speed'])
