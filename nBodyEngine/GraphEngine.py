import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Graph:
	def __init__(self, bodies, graphLimits, graphs: list = []) -> None:
		self.bodies: list = bodies
		self.graphLimits: float = graphLimits
		self.graphs: list = graphs
		self.hasMultipleGraphs:bool = False
		self.graphsPositions: list = []
		self.graphsData: list = [{},{},{}] 
		'''quetsa lista contine un dict per ogni attributo possibile (per ora 3)
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
		self.constructGraphsData()

		# se ci sono dei grafici extra da inserire crea graph data con tante liste vuote quanti grafici extra ci sono 
		if len(graphs) in [1,2]: rows, cols = 1, len(graphs)+1
		elif len(graphs) == 3: rows, cols = 2,2
		self.hasMultipleGraphs = (graphs != [])			# ha più di un grafico?
		if not self.hasMultipleGraphs: rows, cols = 1,1	# se no col e row sono 1

		self.rows = rows
		self.cols = cols
		self.fig, self.ax = plt.subplots(nrows = rows, ncols = cols)
		self.constructGraphsPosition()

	def constructGraphsPosition(self) -> None:
		'''determina le dimensioni di GraphsPosition con cols e rows'''

		if self.cols == 1: # se non ci sono altri grafici mette 
			self.graphsPositions = [self.ax]
			return

		self.graphsPositions: list = []
		graphsLenght: int = len(self.graphs)

		if graphsLenght in [1,2]:
			self.cols, rows= graphsLenght+1, 1
			self.graphsPositions = [self.ax[i] for i in range(len(self.graphs)+1)]
			del graphsLenght
			return

		for x in range(2):
			for y in range(2):
				self.graphsPositions.append(self.ax[x,y])

	def constructGraphsData(self) -> None:
		for attributes in range(len(self.graphsData)):
			for bodies in range(len(self.bodies)):
				self.graphsData[attributes][bodies] = []

	def updateScreen(self) -> None:
		#pulisce tutti i grafici
		_ = self.graphsPositions[0]
		_.clear()
		_.set_xlim(-self.graphLimits, self.graphLimits)
		_.set_ylim(-self.graphLimits, self.graphLimits)
		_.set_aspect('auto')
		_.set_xlabel('x (m)')
		_.set_ylabel('y (m)') # se c'è più di un grafico deve usare la notazione ax[x,y]
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
			dt = 360*24#self.timescale*2e-20
			body.update(dt)
	
	def start(self, timescale) -> None:
		self.timescale: float = timescale
		self.updateScreen()
		ani = FuncAnimation(self.fig, self.animate, frames=30, interval=10)

		plt.show()
