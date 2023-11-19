import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from .Grid import *

class Graph:
	def __init__(self, graphLimits, graphs: list = [], bodies = [], pathTracing = False, dimensions = 2 , toggleInstableOrbits: bool = False, toggleCommonCenter: bool = True, useGrid = True, nOfCells = 5) -> None:
		self.bodies: list = bodies
		self.graphLimits: float = graphLimits
		self.graphs: list[int , ...] = graphs
		self.hasMultipleGraphs:bool = False
		self.nOfGraphs: int = len(graphs)
		self.IOvisible: bool = toggleInstableOrbits # decide se mostrare o meno le orbite instabili
		self.showCenter = toggleCommonCenter
		self.is2d = (dimensions <= 2) 
		self.dimensions = dimensions
		self.pathTracing = pathTracing
		self.useGrid = useGrid
		if useGrid:
			assert nOfCells != 0, "Cannot have 0 cells in a grid, modify this value with the nOfCells attribute"
			self.grid = Grid(3, graphLimits)

		if dimensions > 2 and self.nOfGraphs > 2: raise NotImplementedError("having more than 2 graphs with a 3d simulation is not supported yet")

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
		assert self.nOfGraphs <= 3, f"You cannot put more than three graphs in the same simulation. You tried to put {self.nOfGraphs}"

		if self.nOfGraphs in [1,2]: rows, cols = 1, self.nOfGraphs+1
		elif self.nOfGraphs == 3: rows, cols = 2,2		
		if graphs == []: rows, cols = 1,1	# se ha solo un grafico col e row sono 1

		self.rows: int = rows
		self.cols: int = cols
		self.graphsPositions: list = self.constructGraphsPosition()
		self.graphsData = self.constructGraphsData()

	def constructGraphsPosition(self) -> list:
		'''determina le dimensioni di GraphsPosition con cols e rows'''
		if self.is2d:
			self.fig, self.ax = plt.subplots(self.rows, self.cols)
			return [self.ax] if self.nOfGraphs == 0 else self.ax.flatten()
		
		self.fig = plt.figure()
		res = []

		for x in range(self.cols):
			for y in range(self.rows):
				if x + y == 0:
					res.append(self.fig.add_subplot(121, projection = '3d'))
					continue
				fid = int( f'{x+1}1{y+1}' )
				res.append(self.fig.add_subplot(y+1, x+1, 2))

		self.fig.subplots_adjust(wspace=1, hspace=-.2)

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
		if not self.is2d:
			_.set_aspect('auto') 
			_.auto_scale_xyz([-self.graphLimits, self.graphLimits], [-self.graphLimits, self.graphLimits], [-self.graphLimits, self.graphLimits])
			self.graphsPositions[0].plot(self.graphLimits, self.graphLimits, self.graphLimits, 'o', markersize=1, color='red')
			self.graphsPositions[0].plot(-self.graphLimits, -self.graphLimits, -self.graphLimits, 'o', markersize=1, color='red')	
		else:			
			_.set_aspect('auto')
			_.set_xlim(-self.graphLimits, self.graphLimits)
			_.set_ylim(-self.graphLimits, self.graphLimits)

		_.set_xlabel('x (m)')
		_.set_ylabel('y (m)')
		del _

		'''il pezzo sotto va in ogni grafico (self.graphs), poi in ogni corpo e aggiorna
		la i dati in self.graphsData. ad esempio se self.graphs = [0,1,2] allora graphs data[0]
		registra l'attributo 0 di ogni corpo e cosi via '''

		for x in range(1,len(self.graphsPositions)):
			self.graphsPositions[x].clear()

			for j in range(len(self.bodies)):
				thing = self.graphsData[x-1][j]
				thing.append(self.bodies[j].getAttribute(self.graphs[x-1]))
				self.graphsPositions[x].plot(range(len(self.graphsData[x-1][j])), self.graphsData[x-1][j])
				
	def animate(self, i) -> None:
		self.updateScreen()
		#calcola le forze per tutti i corpi	

		if self.showCenter:
			pos = self.bodies[0].center
			if np.sqrt(sum(pos**2)) < self.graphLimits:
 				self.graphsPositions[0].plot(*pos, '+', color = 'red')
 				
		for body in self.bodies:
			pos = body.position
			self.graphsPositions[0].plot(*pos, 'o', markersize=body.getMarkerSize(self.graphLimits), color=body.color)
			
			if self.pathTracing:
				self.paths[body][0].append(pos[0])
				self.paths[body][1].append(pos[1])
				plt.plot(self.paths[body][0], self.paths[body][1], linestyle='-', color='blue')

			if self.IOvisible and self.is2d: 
				markerPos = [body.position[i] for i in range(len(body.position))]
				marker_circle = plt.Circle((markerPos), body.convert2Screen(self.graphLimits, body.instableOrbitThreshold), edgecolor='black', facecolor='none')
				self.graphsPositions[0].add_patch(marker_circle)
			body.update(self.timescale)
	
	def start(self, timescale) -> None:
		self.timescale: float = timescale

		if self.pathTracing: 
			self.paths = {}
			for body in self.bodies: self.paths[body] = ([],[])

		self.updateScreen()
		self.ani = FuncAnimation(self.fig, self.animate, frames=1650, interval=1000/30)

		plt.show()
