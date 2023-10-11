
from Physics import PointMass2, World2
import DrawingPygame

settings={"timestep":0.01, 
          "width":800, 
          "height":500, 
          "nbody":False,
          "verticalGravity":False,
          "bodyCollissions":True,
          "screenCollissions":True}

print(settings["height"])

li = []
li.append(PointMass2(1, 50, 50, 30, 15, 10))
li.append(PointMass2(1, 100, 150, 30, 0, 0))
li.append(PointMass2(1, 200, 200, 30, 0, 0))
world = World2(li)
DrawingPygame.RUNSIM2(world, settings)

