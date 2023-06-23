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

		self.bodies: list[Body, ...] = bodies
		self.useAccurateSize: bool = useAccurateSize
		
		self.isBlackHole: bool = (self.radius <= 2*self.m*G/c**2) & canBeBH
		if len(infos) == 7: 
			self.color = infos[6]
			return
		self.color: str = 'blue'

	def getAttribute(self, attr: int) -> float: # new
		'''ritorna un attributo a seconda del numero''' # si potrebbe fare in un altro modo con una lista in update ma è troppo poco efficente
		assert attr in [0,1,2], f"invalid input: it must be 0, 1 or 2 not {attr}"
		if attr == 0: return abs(self.vx)+abs(self.vy)			#velocità
		if attr == 1: return self.getAttribute(0)**2*self.m*.5	#energia cinetica
		res: float = 0
		for _ in self.bodies: 				# se questo codice viene eseguito  vuoldire che attr != [0,1]
			if _ == self: continue 			# esclude se stesso
			res += -self.m*_.m*G/self.getDistance(_.x, _.y)[0]
			return res			

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
		self.getSecondPNE(self.bodies)

		self.getAttribute(0)
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

	def getSecondPNE(self, bodies):
		vec = [0,0]
		for i in bodies:
			# calcola il semiasse maggiore
			a = G* i.m / (2 * G - self.getDistance(i.x, i.y)[0] * self.Velocity**2)

			# calcola il semiasse minore
			v_rad = (self.x * self.vx + self.y * self.vy) / np.sqrt(self.x**2 + self.y**2) # velocità radiale
			h = self.x * self.vy - self.y * self.vx # momento angolare specifico
			E = (self.vx**2 + self.vy**2) / 2 - G * i.m / self.Velocity # e specifica
			b = h**2 / (G * i.m * (1 - E**2))

			if a < self.getDistance(i.x, i.y)[0]: continue

			# calcola l'eccentricità
			e = np.sqrt(1-a/b) 

			# calcolo delta pheda
			delta_pheda = (6*float(np.pi)*G*i.m) / (c**2 * a * (1 - e**2))

			Fx_precession = delta_pheda * self.Velocity * self.m * self.vy / self.getDistance(i.x, i.y)
			Fy_precession = -delta_pheda * self.Velocity * self.m * self.vx / self.getDistance(i.x, i.y)

			vec[0] += Fx_precession
			vec[1] += Fy_precession
			
		vec[0] /= len(bodies)
		vec[1] /= len(bodies)
			
	def getDistance(self, x, y) -> tuple[float, ...]:
		'''calcola la distanza tra se stesso e un punto'''
		dx = abs(x - self.x)
		dy = abs(y - self.y)
		return np.sqrt(dx**2 + dy**2), dx, dy

	@property
	def Velocity(self):
		return np.sqrt(self.vy**2 + self.vx**2)

	def getDirectionVector(self, x, y) -> float:
		'''calcola il vettore direzione'''
		myposition = np.array([self.x, self.y])
		itsposition = np.array([x,y])

		return (myposition-itsposition) / np.linalg.norm(myposition - itsposition)
