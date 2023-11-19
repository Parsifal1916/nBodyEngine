from .Body import Body 
from .GraphEngine import Graph
import json
from numpy import sqrt
import os

print('nBodyEngine Installed Successfully!')

def simulateFromJson(jsonFile: str) -> None:
	print('loading json file...')
	with open(jsonFile, 'r') as file:
		content = json.load(file) # estrae il contenuto del file

		#comincia la simulazione
		simulation=Graph(
			content['Simulation']['size'], 
			graphs = content['Simulation']['graphs'], 
			toggleInstableOrbits = content['Simulation'].get('toggleInstableOrbits', False),
			pathTracing = content['Simulation'].get('pathTracing', False),
			dimensions = content['Simulation'].get('style', 2),
			useGrid = content['Simulation'].get('useGrid', False),
			nOfCells = content['Simulation'].get('nOfCells', 3),
		)

		#crea i corpi
		bodies: list = []
		_bodies: list = content['Bodies']
		for i in _bodies:
			try: useAccurateSize = content['Simulation']['useAccurateSize']
			except KeyError: useAccurateSize = False
			bodies.append(Body(
				simulation,
				i, 
				useAccurateSize = content['Simulation'].get('useAccurateSize', False),
				includeSR = content['Simulation'].get('includeSR', False),
				dimensions = content['Simulation'].get('style', 2),
				))
		
		del _bodies
		simulation.bodies = bodies

		if content.get("Cloud") != None:
			for i in content.get("Cloud"):
				cloud(
					simulation,
					i.get("position"),
					i.get("avrMass"),
					i.get("radius"),
					i.get("particles"),
					avrParticleRadius = i.get("avrParticleRadius", 0),
					maxSpeed = i.get("maxSpeed", 0)
					)

	

		print('starting the simulation..')
		simulation.start(content['Simulation']['speed'])

def cloud(simulation, pos: list, avrMass: float, radius: float, particles: int, avrParticleRadius = 0,maxSpeed = 0, massDistributionFunction = None):
		from random import uniform
		for _ in range(particles):
			vel = [uniform(-maxSpeed, maxSpeed) for _ in range(3-simulation.is2d)]
			pos = [uniform(-radius, radius)+pos[i] for i in range(3-simulation.is2d)]
			simulation.bodies.append(Body(
				simulation,
				[avrMass if not massDistributionFunction else massDistributionFunction(avrMass, pos),
				pos,
				vel,
				simulation.graphLimits/100 if avrParticleRadius == 0 else avrParticleRadius]
				))
