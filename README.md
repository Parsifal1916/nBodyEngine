# nBodyEngine
## Description
**nBodyEngine** is an open-source module for simulating the famous n-Body Problem, the orbits of planets around their star and, in future versions, matter falling into a supermassive black hole. The following libraries are required to run the module correctly:
- **matplotlib**
- **numpy**

## Code Overview
### Body Class
The **nBodyEngine.Body** class is used to represent celestial bodies. This class requires two lists, the first is composed of the following arguments (in order):
- Mass of the body
- x position (in meters)
- y position (in meters)
- x velocity (in m/s)
- y velocity (in m/s)
- (optional) marker color for visualization in the graph
The second list contains all nBodyEngine.Body objects present in the simulation.

The class contains the following functions:

- **nBodyEngine.Body.update(dt)**: Updates the position (**self.x** and **self.y**) based on the velocity value (**self.vx** and **self.vy**).

- **nBodyEngine.Body.net_force()**: Calculates the force exerted by all other bodies in the simulation on the given body. Returns two floats (**nBodyEngine.Body.fy** and **nBodyEngine.Body.fx**).

- **nBodyEngine.Body.GetDistance(x, y)**: Calculates the distance between the given body and a given coordinate. Used to calculate gravitational attraction between bodies.

- **nBodyEngine.Body.getDirectionVector(x, y)**: Calculates the x and y components of a force from the given coordinates.

### GraphEngine.py
This script contains the Graph class which requires the following arguments (in order):

- bodies, a list of all bodies in the simulation
- graphLimits, a float representing the dimensions of the graph

The class contains the following functions:

- **nBodyEngine.Graph.updateScreen()**: Clears the screen and resets the graph dimensions.

- **nBodyEngine.Graph.animate()**: Automatically called by matplotlib, updates the position of all bodies with their **update()** method.

- **nBodyEngine.Graph.start(timescale)**: Starts the simulation, requires a parameter (timescale) representing the speed of the simulation.

## Simulating from a json file

The **nBodyEngine.simulateFromJson(jsonFile)** function allows to start a simulation directly from a Json file. This file must be structured as follows:

```json
{
	"Bodies":[
    bodies,
	],
	"Simulation":{
		"speed": speed,
		"size": size
	}
}
```
Replacing '**bodies**' with the list of bodies in the simulation, these bodies will be represented as simply the first input of **nBodyEngine.Body()**. For example:
```json{
	"Bodies":[
    [1.98e87, 0, 0, 0, 0],
	],
	"Simulation":{
		"speed": speed,
		"size": size
	}
}
```

(where in the simulation there is only one body with a mass of 1.98e87 kg, x and y positions of 0, and x and y velocities of 0). '**speed**' and '**size**' are respectively the speed of the simulation (timescale) and the size of the graph (graphLimits).

### Example
This function can be used as follows:
```python
import nBodyEngine as be

be.simulateFromJson(path)
```
where '**path**' is the file path starting from C:/
