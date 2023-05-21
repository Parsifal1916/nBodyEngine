import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Graph:
	def __init__(self, bodies, graphLimits, graphs: list = []) -> None:
		self.bodies: list = bodies
		self.graphLimits: float = graphLimits
		self.graphs: list[int , ...] = graphs
		self.hasMultipleGraphs:bool = False
		self.nOfGraphs: int = len(graphs)

		'''questa lista conteine un dict per ogni attributo possibile (per ora 3)
		   i dict contengono n del corpo : [grafico]
			{
				[0] : {
					1 : [attr, attr]
					2 : [attr, attr]
				}
				[1] : {
					1 : [attr, attr]
					2 : [attr, attr]
				}
			}
		   '''

		# se ci sono dei grafici extra da inserire crea graph data con tante liste vuote quanti grafici extra ci sono 
		assert self.nOfGraphs <= 3, f"You cannot put more than three graphs in the simulation. Tou tried to put {self.nOfGraphs}"

		if self.nOfGraphs in [1,2]: rows, cols = 1, self.nOfGraphs+1
		elif self.nOfGraphs == 3: rows, cols = 2,2		
		if graphs == []: rows, cols = 1,1	# se ha solo un grafico col e row sono 1

		self.rows: int = rows
		self.cols: int = cols
		self.fig, self.ax = plt.subplots(nrows = rows, ncols = cols)
		self.graphsPositions: list = self.constructGraphsPosition()
		self.graphsData = self.constructGraphsData()

	def constructGraphsPosition(self) -> list:
		'''determina le dimensioni di GraphsPosition con cols e rows'''

		if not self.nOfGraphs: 
			return [self.ax] # se non ci sono altri grafici mette 

		if self.nOfGraphs in [1,2]: 
			return [self.ax[i] for i in range(self.nOfGraphs+1)]
		res: list = []

		for x in range(2):
			for y in range(2):
				res.append(self.ax[x,y])
		return res

	def constructGraphsData(self) -> list[dict[int, list], ...]:
		res: list[dict[int, list], ...] = [{},{},{}]
		for attributes in range(self.nOfGraphs):
			for bodies in range(len(self.bodies)):
				res[attributes][bodies] = []
		return res

	def updateScreen(self) -> None:
		#pulisce tutti i grafici
		_ = self.graphsPositions[0]
		_.clear()
		_.set_xlim(-self.graphLimits, self.graphLimits)
		_.set_ylim(-self.graphLimits, self.graphLimits)
		_.set_aspect('auto')
		_.set_xlabel('x (m)')
		_.set_ylabel('y (m)')
		del _

		'''il pezzo sotto va in ogni grafico (self.graphs), poi in ogni corpo e aggiorna
		la i dati in self.graphsData. ad esempio se self.graphs = [0,1,2] allora graphs data[0]
		registra l'attributo 0 di ogni corpo e cosi via '''
		
		for x in range(1,len(self.graphsPositions)):
			self.graphsPositions[x].clear()
			
			for j in range(len(self.bodies)):
				self.graphsData[x-1][j].append(self.bodies[j].getAttribute(self.graphs[x-1]))
				self.graphsPositions[x].plot(range(len(self.graphsData[x-1][j])), self.graphsData[x-1][j])
				
	def animate(self, i) -> None:
		self.updateScreen()
		#calcola le forze per tutti i corpi
		for body in self.bodies:
			self.graphsPositions[0].plot(body.x, body.y, 'o', markersize=body.getMarkerSize(self.graphLimits), color=body.color)
			dt = self.timescale
			body.update(dt)
	
	def start(self, timescale) -> None:
		self.timescale: float = timescale
		self.updateScreen()
		ani = FuncAnimation(self.fig, self.animate, frames=30, interval=10)

		plt.show()
