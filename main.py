
from Physics import PointMass2, World2
import DrawingPygame

settings={"timestep":1e4, 
          "width":800, 
          "height":500, 
          "nbody":True,
          "verticalGravity":False,
          "bodyCollissions":False,
          "screenCollissions":True}

print(settings["height"])

li = []
li.append(PointMass2(1, 50, 50, 3, 0, 0))
li.append(PointMass2(1, 100, 150, 3, 0, 0))
li.append(PointMass2(1, 200, 200, 3, 0, 0))
li.append(PointMass2(1, 50, 200, 3, 0, 0))
li.append(PointMass2(1, 350, 50, 3, 0, 0))
li.append(PointMass2(1, 310, 150, 3, 0, 0))
li.append(PointMass2(1, 320, 200, 3, 0, 0))
li.append(PointMass2(1, 350, 200, 3, 0, 0))
world = World2(li)
DrawingPygame.RUNSIM2(world, settings)

