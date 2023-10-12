
from Physics import PointMass2, World2
import DrawingPygame

settings={"timestep":1e6/10, 
          "width":550, 
          "height":550, 
          "nbody":True,
          "verticalGravity":True,
          "bodyCollissions":True,
          "screenCollissions":True}
li = []
if True:
    li.append(PointMass2(2, 50, 52, 4, 0, 0))
    li.append(PointMass2(2, 100, 51, 4, 0, 0))
    li.append(PointMass2(4, 200, 202, 8, 0.000001, 0.000001))
    li.append(PointMass2(4, 50, 205, 8, 0, 0))
    li.append(PointMass2(6, 350, 52,12, 0, 0))
    li.append(PointMass2(6, 310, 155, 12, 0, 0))
    li.append(PointMass2(10, 320, 202, 20, 0.00001, 0))

if False:
    for n in range(7):
        for m in range(5):
            li.append(PointMass2(1, n*40+50, m*40+50, 5, 0, 0))


world = World2(li)
DrawingPygame.RUNSIM2(world, settings)

