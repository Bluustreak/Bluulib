
from Physics import PointMass2, World2
import DrawingPygame
import random

settings = {"timestep": 1e4*2,
            "width": 550,
            "height": 550,
            "nbody": True,
            "verticalGravity": False,
            "bodyCollissions": True,
            "screenCollissions": True,
            "merging": False}

# generate some particles evenly across the world
li = []
if True:
    nw, nh = 2, 2
    for n in range(nw):
        for m in range(nh):
            w, h = settings["width"], settings["height"]
            mass = random.randint(10, 50)
            li.append(PointMass2(mass, w/nw * n + 20, h/nh * m + 20, 0, 0))


world = World2(li)
DrawingPygame.RUNSIM2(world, settings)
