from numpy import floor
def a():...

class Grid:
	def __init__(self, cells, graphLimits,dimensions = 2):
		super(Grid, self).__init__()
		self.graphLimits = graphLimits
		self.grid = {}
		self.cells = cells

		self.initialize2dGrid if dimensions == 2 else self.initialize3dGrif

	def clamp(self, n):
		if n < 0: return 0
		if n > self.cells-1: return self.cells-1
		return n

	def mapToGrid(self, pos): 
		return list(self.clamp(floor(i*self.cells / self.graphLimits)+self.cells-1) for i in pos) 

	@property
	def initialize2dGrid(self):
		for x in range(self.cells):
			for y in range(self.cells):
				self.grid[x,y] = []

	@property
	def initialize3dGrif(self):
		for x in range(self.ells):
			for y in range(self.cells):
				for x in range(self.cells):
					self.grid[x,y,z] = []
					
	def addItem(self, cell, item):
		if item not in self[cell]: self[cell].append(item)

	def __getitem__(self, index):
		return self.grid[self.clamp(index[0]), self.clamp(index[1])]
	def __len__(self): return len(self.grid)
