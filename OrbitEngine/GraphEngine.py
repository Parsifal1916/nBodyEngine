import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numpy import log10

def animate(i):
	#mette i limiti e i label
	ax.clear()
	ax.set_xlim(-graphLimits, graphLimits)
	ax.set_ylim(-graphLimits, graphLimits)
	ax.set_aspect('equal')
	ax.set_xlabel('x (m)')
	ax.set_ylabel('y (m)')

	#calcola le forze per tutti i corpi
	for body in bodies:
		ax.plot(body.x, body.y, 'o', markersize=np.log10(body.m)/10, color=body.color)
		dt = 2e-20
		body.update(dt)

	ani = FuncAnimation(fig, animate, frames=30, interval=10)


def graph(graphLimits, timescale, bodies):
	graphLimits: int = graphLimits
 
	# Set up grid and plot
	fig, ax = plt.subplots()
	ax.set_xlim(-graphLimits, graphLimits)
	ax.set_ylim(-graphLimits, graphLimits)
	ax.set_aspect('equal')
	ax.set_xlabel('x (m)')
	ax.set_ylabel('y (m)')

	for body in bodies:
		ax.plot(body.x, body.y, 'o', markersize=log10(body.m)/10, color=body.color)
		dt = timescale
		body.update(dt)

	ani = FuncAnimation(fig, animate, frames=30, interval=10)

	plt.show()