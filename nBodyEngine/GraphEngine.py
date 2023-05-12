import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import log10



class Graph:
	def __init__(self, bodies, graphLimits):
		self.bodies: list = bodies
		self.graphLimits: float = graphLimits

		self.fig, self.ax = plt.subplots()
		self.updateScreen()


	def updateScreen(self):
		self.ax.clear()
		self.ax.set_xlim(-self.graphLimits, self.graphLimits)
		self.ax.set_ylim(-self.graphLimits, self.graphLimits)
		self.ax.set_aspect('equal')
		self.ax.set_xlabel('x (m)')
		self.ax.set_ylabel('y (m)')	
			
	def animate(self, i):

		self.updateScreen()
		#calcola le forze per tutti i corpi
		for body in self.bodies:
			self.ax.plot(body.x, body.y, 'o', markersize=log10(body.m)/10, color=body.color)
			dt = 2e-20
			body.update(dt)
	
	def start(self, timescale):

		ani = FuncAnimation(self.fig, self.animate, frames=30, interval=10)

		plt.show()