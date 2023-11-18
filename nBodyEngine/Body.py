import numpy as np
from math import atan2

G = 6.67430e-11  # N(m/kg)^2
c = 299_792_458  # m/s velocità della luce

		
class Body:
	def __init__(self, infos: list, bodies: list, canBeBH: bool = True, useAccurateSize: bool = True, includeSR: bool = False, dimensions: int = 2) -> None:
		self.mass: float = infos[0]	# Massa 		kg
		self.position = np.array(infos[1])*1.
		self.velocity = np.array(infos[2])*1.
		self.radius: float = infos[3] # raggio del corpo
		self.dimensions = dimensions
		
		self.a = 0
		
		self.includeSR: bool = includeSR
		
		self.SRmass = self.m * self.gamma

		self.possibleAttributes = [0,1,2,3]
		self.p_TotForce = 0

		self.bodies: list[Body, ...] = bodies
		self.useAccurateSize: bool = useAccurateSize

		# GR setup
		self.schwarzshildRadius = 2*self.m*G/c**2
		self.instableOrbitThreshold = 3*self.schwarzshildRadius
		
		self.isBlackHole: bool = (self.radius <= self.schwarzshildRadius) & canBeBH
		
		# color setup
		if self.isBlackHole: 
			self.color = 'black'
			return 

		if len(infos) == 5: 
			self.color = infos[4]
			return
		self.color: str = 'blue'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++ Vectors ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	
	def pitagora(self, position) -> float:
		return np.sqrt(sum(position**2))

	def getDistance(self, position) -> tuple[float, ...]:
	    '''calcola la distanza tra se stesso e un punto'''
	    deltaP = abs(self.position - position)

	    distance = np.sqrt(sum(deltaP**2))
	    if distance == 0:  # Gestisci il caso in cui la distanza è zero
	        distance = 1e-10 # Imposta una distanza minima diversa da zero

	    return distance, deltaP

	def getDirectionVector(self, position) -> float:
		'''calcola il vettore direzione'''

		return (self.position-position) / np.linalg.norm(self.position-position)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++ Physics ++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def getSecondPNE(self, bodies) -> list[float, ...]:
		totalMass = self.centralMass

		# calcola il baricentro comune
		center = self.center
		
		r, delta = self.getDistance(center) # distanza dal baricentro

		self.a = -G * totalMass / (2 * (self.getAttribute(2) + self.getAttribute(1))/self.m)# semiasse maggiore

		b = r*self.totalVelocity / G*totalMass
        
		if not self.validateInput(self.a,b): return np.array([0. for i in range(self.dimensions)])
        
		e = np.sqrt(np.abs(1 - (b**2 / self.a**2)))

		self.delta_pheda = (6 * np.pi * G * totalMass) / np.where(np.abs(1 - e**2) > 0, (c**2 * self.a * np.abs(1 - e**2)), np.inf)
	        
		precession = np.where(r > 0, self.delta_pheda * self.totalVelocity * self.m * self.velocity / r, 0)
		
		return precession

	def net_force(self) -> np.array:
		'''calcola la forza totale'''
		p_force = np.array([0. for i in range(self.dimensions)])
		for other in self.bodies:
			if other == self: continue 							   # esclude se stesso
			r, delta = self.getDistance(other.position) 		   # ottiene r x calcolare la forza
			f = -G * self.m * other.m / r**2   	  # calcola la forza
			drt = self.getDirectionVector(other.position)		   
			p_force += drt*f # aggiorna la forza
		return p_force

	def update(self,dt) -> np.array:
		''' aggiorna la velocità '''

		self.velocity += (self.getSecondPNE(self.bodies) / self.m)

		# calcola la forza proveniente da tutti i corpi

		self.velocity += (self.net_force() / self.m)

		self.position += self.velocity * dt

		return self.position

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++ Graph Methods ++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	def getAttribute(self, attr: int) -> float: # new
			'''ritorna un attributo a seconda del numero''' # si potrebbe fare in un altro modo con una lista in update ma è troppo poco efficente
			assert attr in self.possibleAttributes, f"invalid input: it must be 0, 1, 2 or 3 not {attr}"
			if attr == 0: return self.totalVelocity		#velocità
			if attr == 1: return self.getAttribute(0)**2*self.m*.5	#energia cinetica
			if attr == 3: return self.a
			# se questo codice viene eseguito  vuoldire che attr != [0,1,3]
			return self.potentialEnergy
	
	def getMarkerSize(self, graphLimits) -> int: 
		'''calcola la grandezza del marker'''
		size = 0
		if not self.useAccurateSize:
			return np.log10(self.m)/10 # se non usa la grandezza accurata mette log10 della massa su 10
		
		size = self.convert2Screen(graphLimits, self.schwarzshildRadius)
		
		if not self.isBlackHole: 
			size = self.convert2Screen(graphLimits, self.radius) #se è un buco nero ritorna il raggio di s
		
		if size > 263: return 263
		return size

	def convert2Screen(self, graphLimits, lenght) -> float:
		return (lenght/graphLimits)*263

	def validateInput(self, *num) -> bool:
		validation = [np.isnan(i) or np.isinf(i) for i in num]
		return not all(validation)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++ Properties +++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	@property 
	def potentialEnergy(self) -> float:
		r = self.getDistance(self.center)[0]

		frequency = self.totalVelocity / ( 2 * np.pi *  r)	

		angularMomentum = 2 * np.pi * frequency * self.m * r**2

		potE = (-G*self.m*self.centralMass/r) + (angularMomentum**2 / 2 * self.m * r**2 ) - ((G*self.centralMass* angularMomentum**2)/self.m*c**2 * r**3)

		return potE	

	@property
	def gamma(self) -> float:
		inverse_gamma = np.sqrt(1 - self.totalVelocity**2 / c**2)
		return 1/inverse_gamma

	@property
	def totalVelocity(self):
		return sum(self.velocity**2)

	@property
	def m(self):
		if not self.includeSR:
			return self.mass
		self.SRmass = self.mass * self.gamma
		return self.SRmass

	@property
	def centralMass(self) -> float:
		return sum([i.m for i in self.bodies])

	@property 
	def center(self) -> tuple[float, float]:
		return sum([body.m * body.position for body in self.bodies]) / sum([body.m for body in self.bodies])
