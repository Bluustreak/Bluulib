import Geometry as g
import math

G=6.67*10**-11
     
class PointMass2():
    def __init__(self, mass, x, y, radius, velocityX, velocityY):
        self.x = x 
        self.y = y 
        self.radius = radius
        self.mass = mass
        self.velocityX = velocityX
        self.velocityY = velocityY
    def getVelocity(self):
        v = g.distance2(0,0, self.velocityX, self.velocityY)
        return v
    
class PointMass3(g.Point3):
    #inherits position
    def __init__(self, mass,x,y,z, velocityX, velocityY, velocityZ):
        super().__init__(x,y,z)
        self.mass = mass
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.velocityZ = velocityZ
    def velocity(self):
        v = g.distance3(0,0,0, self.velocityX, self.velocityY, self.velocityZ)
        return v
    
class World2:
    def __init__(self, lop):
        self.pointsList = lop
    def totalEnergy(self):
        pass
    def update(self, settings):
        ts = settings["timestep"]
        W = settings["width"]
        H = settings["height"]

        if settings["verticalGravity"]:
            grav = 9.8
            for p in self.pointsList:
                p.velocityY += grav*ts

        if settings["screenCollissions"]:
            for p in self.pointsList:
                if p.y-p.radius < 0 or p.y+p.radius > H:
                    p.velocityY*=-1
                if p.x-p.radius < 0 or p.x+p.radius > W:
                    p.velocityX*=-1

        if settings["bodyCollissions"]:
            for p in self.pointsList:
                for other in self.pointsList:
                    if p != other:
                        dist = g.distance2(p.x, p.y, other.x, other.y)
                        collission = dist[0] < (p.radius + other.radius)
                        if collission:
                            speedThis = p.getVelocity()
                            speedOther = other.getVelocity()
                            dvx=speedOther[1]-speedThis[1]
                            dvy=speedOther[2]-speedThis[2]
                            
                            speed = g.distance2b(dvx, dvy)
                            amountx = dist[1]/dist[0]
                            amounty = dist[2]/dist[0]
                            #p.velocityX += amountx*speed
                            #p.velocityY += amounty*speed

                            p.velocityX = speed*amountx*g.sign(dist[1])
                            p.velocityY = speed*amounty*g.sign(dist[2])
        
        if settings["nbody"]:
            option = "UpdateOneAtAtime"

            if option == "UpdateAllAtOnce":
                PLcopy = self.pointsList.deepcopy()
                for p in PLcopy:
                    for other in PLcopy:
                        if p != other:
                            newVel=newVelDue2(p, other)
                            p.velocityX = newVel[0]
                            p.velocityX = newVel[1]
                for n in range(PLcopy.length):
                    self.pointsList[n] = PLcopy[n].deepcopy()

            if option == "UpdateOneAtAtime":
                for p in self.pointsList:
                    for other in self.pointsList:
                        if p != other:
                            newVel=newVelDue2(p, other, ts)
                            p.velocityX = newVel[0]
                            p.velocityY = newVel[1]
            
        #this runs at the end regardless of which you choose, since al lthe functions only update the velocity
        for p in self.pointsList:
            dispX = p.velocityX * ts
            dispY = p.velocityY * ts
            p.x += dispX
            p.y += dispY

        



def forceDue2(p:PointMass2, other:PointMass2):
    dist = g.distance2(p.x, p.y, other.x, other.y)
    resForce = (G * p.mass * other.mass)/dist[2]**2
    return resForce


def accDue2(p:PointMass2, other:PointMass2):
    f=forceDue2(p, other)
    dist=g.distance2(p.x, p.y, other.x, other.y)
    a=f/p.mass
    ax=a*(dist[0]/dist[2])
    ay=a*(dist[1]/dist[2])
    return [ax, ay, a]

def newVelDue2(p:PointMass2, other:PointMass2, ts):
    accXYC = accDue2(p, other)
    velX = accXYC[0]*ts
    velY = accXYC[1]*ts
    return [p.velocityX+velX, p.velocityY+velY]

def dispDue2(p:PointMass2, other:PointMass2, ts):
    acc=accDue2(p, other)
    dispX=p.velocityX + 0.5*acc[0]*ts**2
    dispY=p.velocityY + 0.5*acc[1]*ts**2
    return [dispX, dispY]

def newPosDue2(p:PointMass2, other:PointMass2, ts):
    disp = dispDue2(p, other, ts)
    newX = p.x+disp[0]
    newY = p.y+disp[1]
    return [newX, newY]

