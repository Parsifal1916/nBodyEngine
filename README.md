# nBodyEngine
## Description
**nBodyEngine** is an open-source module for simulating the famous n-Body Problem, the orbits of planets around their star and, in future versions, matter falling into a supermassive black hole. The following libraries are required to run the module correctly:
- **matplotlib**
- **numpy**

## What's new
You can now have 3d simulations by changing the style of the simulation in the json file (see the json file documentation)

## Code Overview
### Body Class
The **nBodyEngine.Body** class is used to represent celestial bodies. This class requires two lists, the first is composed of the following arguments (in order):
- Mass of the body
- [x, y, z]/[x,y] position components (in meters)
- [x, y, z]/[x,y] velocity components (in m/s)
- radius of the body (in meters)
- (optional) marker color for visualization in the graph
The second list contains all nBodyEngine.Body objects present in the simulation.

The class contains the following functions:

- **nBodyEngine.Body.getAttribute(attr)**: depending on the value of '**attr**' it returns a different attribute of the body. it is used by **GraphEngine.py** to graph velocity, kinetic and potential energy. The possible inputs are listed below:
	- **0**: Returns the body's velocity
	- **1**: Returns the body's kinetic Energy
	- **2**: Returns the body's potential Energy
	- Any other number will return **None**

- **nBodyEngine.Body.update(dt)**: Updates the position (**self.x** and **self.y**) based on the velocity value (**self.vx** and **self.vy**).

- **nBodyEngine.Body.net_force()**: Calculates the force exerted by all other bodies in the simulation on the given body. Returns two floats (**nBodyEngine.Body.fy** and **nBodyEngine.Body.fx**).

- **nBodyEngine.Body.GetDistance(x, y)**: Calculates the distance between the given body and a given coordinate. Used to calculate gravitational attraction between bodies.

- **nBodyEngine.Body.getDirectionVector(x, y)**: Calculates the x and y components of a force from the given coordinates.

- **nBodyEngine.Body.getMarkerSize(graphLimits)**: Calculates the size of the marker according to the size of the graph (graphLimits) and the radius of the object; it will return a number based on the mass if '**useAccurateSize**' is set to false.

- **nBodyEngine.Body.pitagora(x, y)**: Returns the sqrt of x^2 + y^2

- **nBodyEngine.Body.getSecondPNE()**: Calculates the precession of the body around the common baricenter. It returns a list containing the force along the x axis and y axis

- **nBodyEngine.Body.convert2screen()**: Is an internal function used to convert a lenght in meters to a proportional scale for the markers on screen

-  **nBodyEngine.Body.validateInput(num)**: It takes in a large number of variables and returns True if all values are not infinite or NaN, False otherwise

You can also set these optional boolean values:
- **canBeBH**, is used to enable/disable black holes
- **useAccurateSize**, it will be defaulted to True, see **nBody.Body.getMarkerSize**

This class has also the following properties:
-  **nBodyEngine.Body.potentialEnergy**: Is the relativistic potential energy
-  **nBodyEngine.Body.Velocity**: Is the body's velocity
-  **nBodyEngine.Body.center**: Is the common baricenter in terms of x and y
-  **nBodyEngine.Body.centralMass**: Is the combined mass of all the bodies in the simulation

### GraphEngine.py
This script contains the Graph class which requires the following arguments (in order):

- bodies, a list of all bodies in the simulation
- graphLimits, a float representing the dimensions of the graph

The class contains the following functions:

- **nBodyEngine.Graph.constructGraphsPosition()**: An internal function used to map the array of graphs in order to make it easier for **updateScreen()** to display data about the simulation.

- **nBodyEngine.Graph.constructGraphsData**: An internal function used to map bodies and the corresponding attributes.

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
		"useAccurateSize": 1
	}
}
```
Replacing '**bodies**' with the list of bodies in the simulation, these bodies will be represented as simply the first input of **nBodyEngine.Body()**. For example:
```json
{
	"Bodies":[
    [1.98e87, 0, 0, 0, 0],
	],
	"Simulation":{
		"speed": speed,
		"size": size,
		"useAccurateSize": 1,
		"toggleInstableOrbits" : true,
		"toggleCommonCenter" : true,
		"style" : 2
	}
}
```
where:
- **speed** is the speed of the simulation
- **size** is the size of the simulation (in meters)
- if **useAccurateSize** is set to 1 means that you have inserted a radius, otherwise nBodyEngine will calculate it by itself. see **nBodyEngine.Body.getMarkerSize**.
- **toggleInstableOrbits** will show a circle corrisponding to 3 x the schwarzshild radius if set to true.
- **toggleCommonCenter** shows a little '+' marker where the common center of mass is.
- **style** is the number of dimensions of the simulation (2 or 3)
(in this case, in the simulation there is only one body with a mass of 1.98e87 kg, x and y positions of 0, and x and y velocities of 0)

### Example
This function can be used as follows:
```python
import nBodyEngine as be

be.simulateFromJson(path)
```
where '**path**' is the file path starting from C:/. You can also add the parameter '**graphs**', it is a list of additional graphs that will be added to the simulation as shown below. 
![image](https://github.com/Parsifal1916/nBodyEngine/assets/120274850/d8b033d2-87ca-4e60-90f3-5f5a7cda08a7)
This list must have a length of 3 elements maximum (since there are only 3 attributes to show). Those elements must be valid inputs for the **nBodyEngine.Body.getAttribute(attr)**'.
```json
{
	"Bodies":[
    [1.98e87, 0, 0, 0, 0],
	],
	"Simulation":{
		"speed": speed,
		"size": size
		"useAccurateSize": 1,
		"graph": [0,1,2],
		"style": 2
	}
}
```
In this example we create a simulation with all three attributes shown. You can change the order and the amount of attributes as you wish.
