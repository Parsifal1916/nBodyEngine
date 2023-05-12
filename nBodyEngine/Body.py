import numpy as np

G = 6.67430e-11  # N(m/kg)^2

class Body:
	def __init__(self, infos: list, bodies: list) -> None:
		self.m = infos[0]	# Massa 		kg
		self.x = infos[1]	# posizione y	m
		self.y = infos[2]   # posizione x 	m
		self.vx = infos[3]  # velocità x 	m/s
		self.vy = infos[4]  # velocità y	m/s
		self.bodies = bodies

		if len(infos) == 5:
			self.color = "black"
			return
		self.color = infos[5]

	def update(self,dt):
		''' aggiorna la velocità '''
		fx, fy = self.net_force()
		self.vx += fx / self.m * dt
		self.vy += fy / self.m * dt 

		# aggiorna la posizione
		self.x += self.vx * dt 
		self.y += self.vy * dt

	def net_force(self):
		'''calcola la forza totale'''
		p_force = np.array([0.,0.])
		for other in self.bodies:
			if other == self: continue 							   # esclude se stesso
			r, dx, dy = self.getDistance(other.x, other.y) 		   # ottiene r x calcolare la forza
			f = -G * self.m * other.m / r**2   					   # calcola la forza
			p_force += self.getDirectionVector(other.x, other.y)*f # aggiorna la forza
		return p_force[0], p_force[1]

	def getDistance(self, x, y) -> float:
		'''calcola la distanza tra se stesso e un punto'''
		dx = abs(x - self.x)
		dy = abs(y - self.y)
		return np.sqrt(dx**2 + dy**2), dx, dy

	def getDirectionVector(self, x, y):
		'''calcola il vettore direzione'''
		myposition = np.array([self.x, self.y])
		itsposition = np.array([x,y])

		return (myposition-itsposition) / np.linalg.norm(myposition - itsposition)