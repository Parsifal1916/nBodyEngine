import numpy as np

G = 6.67430e-11  # N(m/kg)^2
c = 299_792_458  # m/s velocità della luce


class Body:
	def __init__(self, infos: list, bodies: list, canBeBH: bool = True, useAccurateSize: bool = True) -> None:
		self.m: float = infos[0]	# Massa 		kg
		self.x: float = infos[1]	# posizione y	m
		self.y: float = infos[2]   # posizione x 	m
		self.vx: float = infos[3]  # velocità x 	m/s
		self.vy: float = infos[4]  # velocità y	m/s
		self.radius: float = infos[5] # raggio del corpo

		self.possibleAttributes = [0,1,2,3]
		self.p_TotForce = 0

		self.bodies: list[Body, ...] = bodies
		self.useAccurateSize: bool = useAccurateSize
		
		self.isBlackHole: bool = (self.radius <= 2*self.m*G/c**2) & canBeBH
		if len(infos) == 7: 
			self.color = infos[6]
			return
		self.color: str = 'blue'

	def getAttribute(self, attr: int) -> float: # new
		'''ritorna un attributo a seconda del numero''' # si potrebbe fare in un altro modo con una lista in update ma è troppo poco efficente
		assert attr in self.possibleAttributes, f"invalid input: it must be 0, 1, 2 or 3 not {attr}"
		if attr == 0: return self.Velocity		#velocità
		if attr == 1: return self.getAttribute(0)**2*self.m*.5	#energia cinetica
		if attr == 3: return self.p_TotForce
		res: float = 0
		for _ in self.bodies: 				# se questo codice viene eseguito  vuoldire che attr != [0,1]
			if _ == self: continue 			# esclude se stesso
			res += -self.m*_.m*G/self.getDistance(_.x, _.y)[0]
		return res		

	@property 
	def Velocity(self):
		return np.sqrt(self.vx**2 + self.vy**2)

	def pitagora(self, x, y):
		return np.sqrt(float(x)**2 + float(y)**2)

	def getSecondPNE(self, bodies):
		vec = [0, 0]

		totalMass = sum([i.m for i in bodies])

		# calcola il baricentro comune
		center_x = sum([body.m * body.x for body in bodies]) / sum([body.m for body in bodies])
		center_y = sum([body.m * body.y for body in bodies]) / sum([body.m for body in bodies])
 		
		r, dx, dy = self.getDistance(center_x, center_y) # distanza dal baricentro

		a = -G * totalMass / (2 * (self.getAttribute(2) + self.getAttribute(1))/self.m)# semiasse maggiore

		b = r*self.Velocity / G*totalMass
        
		#if np.isnan(a) or np.isnan(b) or np.isinf(a) or np.isinf(b): continue
        
		e = np.sqrt(np.abs(1 - (b**2 / a**2)))

		self.delta_pheda = (6 * np.pi * G * totalMass) / np.where(np.abs(1 - e**2) > 0, (c**2 * a * np.abs(1 - e**2)), np.inf)
	        
		Fx_precession = np.where(r > 0, self.delta_pheda * self.Velocity * self.m * self.vy / r, 0)
		vec[0] += Fx_precession
	
		Fy_precession = np.where(r > 0, -self.delta_pheda * self.Velocity * self.m * self.vx / r, 0)
		vec[1] += Fy_precession

		self.p_TotForce = np.sqrt(Fy_precession**2 + Fx_precession**2)
	    
		return vec


	def getMarkerSize(self, graphLimits) -> int: 
		'''calcola la grandezza del marker'''
		size = 0
		if not self.useAccurateSize:
			return np.log10(self.m)/10 # se non usa la grandezza accurata mette log10 della massa su 10
	
		if not self.isBlackHole: 
			size = (self.radius/graphLimits)*263 #se è un buco nero ritorna il raggio di s
		size = (2*self.m*G/c**2/graphLimits)*263 
		if size > 263: return 263 

	def update(self,dt):
		''' aggiorna la velocità '''

		precX, precY = self.getSecondPNE(self.bodies)


		self.vx += (precX / self.m) * dt
		self.vy += (precY / self.m) * dt

		fx, fy = self.net_force()
		self.vx += fx / self.m * dt
		self.vy += fy / self.m * dt 

		# aggiorna la posizione
		self.x += self.vx * dt 
		self.y += self.vy * dt

	def net_force(self) -> tuple[float, ...]:
		'''calcola la forza totale'''
		p_force = np.array([0.,0.])
		for other in self.bodies:
			if other == self: continue 							   # esclude se stesso
			r, dx, dy = self.getDistance(other.x, other.y) 		   # ottiene r x calcolare la forza
			f = -G * self.m * other.m / r**2   					   # calcola la forza
			p_force += self.getDirectionVector(other.x, other.y)*f # aggiorna la forza
		return p_force[0], p_force[1]

	def validateInput(self, *num):
		validation = [np.isnan(i) or np.isinf(i) for i in num]
		return not all(validation)

	def getDistance(self, x, y) -> tuple[float, ...]:
	    '''calcola la distanza tra se stesso e un punto'''
	    dx, dy = 1, 1 # valori di default

	    if self.validateInput(x, self.x):
	        dx = abs(x - self.x)

	    if self.validateInput(y, self.y):
	        dy = abs(y - self.y)

	    distance = self.pitagora(dx, dy)
	    if distance == 0:  # Gestisci il caso in cui la distanza è zero
	        return 1e-10, dx, dy  # Imposta una distanza minima diversa da zero

	    return distance, dx, dy

	def getDirectionVector(self, x, y) -> float:
		'''calcola il vettore direzione'''
		myposition = np.array([self.x, self.y])
		itsposition = np.array([x,y])

		return (myposition-itsposition) / np.linalg.norm(myposition - itsposition)
