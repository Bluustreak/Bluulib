
from Physics import PointMass2, World2
import DrawingPygame
import random

settings = {"timestep": 1e4*2,
            "width": 1500,
            "height": 900,
            "nbody": True,
            "verticalGravity": False,
            "bodyCollissions": True,
            "screenCollissions": True,
            "merging": True}

# generate some particles evenly across the world
li = []
if True:
    nw, nh = 10, 10
    for n in range(nw):
        for m in range(nh):
            w, h = settings["width"], settings["height"]
            mass = random.randint(10, 100)
            speedX = (random.randint(0,10)-5)/1e5
            speedY = (random.randint(0,10)-5)/1e5
            li.append(PointMass2(mass, w/nw * n + 20, h/nh * m + 20, speedX, speedY))

li[random.randint(0,nw*nh-1)].color= (240, 117, 152)
li[random.randint(0,nw*nh-1)].color= (102, 167, 232)
world = World2(li)
DrawingPygame.RUNSIM2(world, settings)
