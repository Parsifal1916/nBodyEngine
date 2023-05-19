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

		# se ci sono dei grafici extra da inserire crea graph data con tante liste vuote quanti grafici extra ci sono 
		if len(graphs) in [1,2]: rows, cols = 1, len(graphs)
		elif len(graphs) == 3: rows, cols = 2,2
		self.hasMultipleGraphs = (graphs != [])			# ha più di un grafico?
		if not self.hasMultipleGraphs: rows, cols = 1,1	# se no col e row sono 1



		self.rows = rows
		self.cols = cols
		self.fig, self.ax = plt.subplots(nrows = rows, ncols = cols)
		
		if cols == 1: # se non ci sono altri grafici mette 
			self.graphsPositions = [self.ax]
			return

		self.graphsPositions: list = []
		graphsLenght: int = len(graphs)

		if graphsLenght in [1,2]:
			cols = graphsLenght+1
			rows = 1
			self.graphsPositions = [[self.ax[i]] for i in range()]
			del graphLimits
			return

		for x in range(2):
			for y in range(2):
				self.graphsPositions.append(self.ax[x,y])

	def updateScreen(self) -> None:
		#pulisce tutti i grafici
		self.graphsPositions[0].set_xlim(-self.graphLimits, self.graphLimits)
		self.graphsPositions[0].set_ylim(-self.graphLimits, self.graphLimits)
		self.graphsPositions[0].set_aspect('equal')
		self.graphsPositions[0].set_xlabel('x (m)')
		self.graphsPositions[0].set_ylabel('y (m)') # se c'è più di un grafico deve usare la notazione ax[x,y]
		
		'''il pezzo sotto va in ogni grafico (self.graphs), poi in ogni corpo e aggiorna
		la i dati in self.graphsData. ad esempio se self.graphs = [0,1,2] allora graphs data[0]
		registra l'attributo 0 di ogni corpo e cosi via '''
		
		for x in range(self.cols-1):
			self.graphsPositions[x].clear()
			for j in self.bodies:
				self.graphsData[x].append(j.getAttribute(self.graphs[x]))
				self.graphsPositions[x].plot(self.graphsData[x], np.array(0,len(self.graphsData[x])), label = f'Body {x+1}')

		#aggiorna posizione e dimensione del primo grafico (quello con la simulazione)
		
		plt.legend()

	def animate(self, i) -> None:
		self.updateScreen()
		#calcola le forze per tutti i corpi
		for body in self.bodies:
			self.graphsPositions[0].plot(body.x, body.y, 'o', markersize=body.getMarkerSize(self.graphLimits), color=body.color)
			dt = self.timescale*2e-20
			body.update(dt)
	
	def start(self, timescale) -> None:
		self.timescale: float = timescale
		self.updateScreen()
		ani = FuncAnimation(self.fig, self.animate, frames=30, interval=10)

		plt.show()
