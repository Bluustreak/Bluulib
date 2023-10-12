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
        self.prevX
        self.prevY
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
        self.collissions = 0
    def totalEnergy(self):
        pass
    def update(self, settings):
        ts = settings["timestep"]
        W = settings["width"]
        H = settings["height"]

        if settings["verticalGravity"]:
            grav = 9.8/1e14
            for p in self.pointsList:
                p.velocityY += grav*ts

        if settings["screenCollissions"]:
            bounceEnergyLoss = 0.1
            for p in self.pointsList:
                if p.y-p.radius < 0:
                    p.y=0+p.radius
                    p.velocityY*=-(1-bounceEnergyLoss)
                elif p.y+p.radius > H:
                    p.y=H-p.radius
                    p.velocityY*=-(1-bounceEnergyLoss)
                if p.x-p.radius < 0:
                    p.x=0+p.radius
                    p.velocityX*=-(1-bounceEnergyLoss)
                elif p.x+p.radius > W:
                    p.x=W-p.radius
                    p.velocityX*=-(1-bounceEnergyLoss)

        if settings["bodyCollissions"]:
            bounceEnergyLoss = 0.2
            for p in self.pointsList:
                for other in self.pointsList:
                    if p != other:
                        dist = g.distance2(p.x, p.y, other.x, other.y)
                        collission = dist[2] < (p.radius + other.radius)
                        if collission:
                            p.x = p.prevX
                            p.y = p.prevY
                            speedThis = p.getVelocity()
                            speedOther = other.getVelocity()
                            dvx=speedThis[0]-speedOther[0]
                            dvy=speedThis[1]-speedOther[1]
                            relativeSpeed = g.distance2b(dvx, dvy)
                            velScalarX = (1-bounceEnergyLoss*(dvx/relativeSpeed))
                            velScalarY = (1-bounceEnergyLoss*(dvy/relativeSpeed))

                            option = 2
                            if option == 1:
                                speedThis = p.getVelocity()
                                speedOther = other.getVelocity()
                                dvx=speedOther[1]-speedThis[1]
                                dvy=speedOther[2]-speedThis[2]
                                relativeSpeed = g.distance2b(dvx, dvy)

                                collissionEnergy = relativeSpeed*p.mass/2

                                angleOfContact = math.atan2(other.x-p.x, other.y-p.y)*(180/3.14156)-90
                                angleOfDirection = math.atan2(p.velocityX, p.velocityY)*(180/3.14156)

                                newAngleOfDirection = angleOfContact-angleOfDirection
                                newXspeed = math.cos(newAngleOfDirection)*(collissionEnergy/p.mass)
                                newYspeed = math.sin(newAngleOfDirection)*(collissionEnergy/p.mass)
                                p.velocityX = newXspeed
                                p.velocityY = newYspeed
                            elif option == 2:
                                dist = g.distance2(p.x, p.y, other.x, other.y)
                                f = (G*p.mass*other.mass) / (dist[2])*-1
                                accx = f/p.mass*(dist[0]/dist[2])
                                accy = f/p.mass*(dist[1]/dist[2])
                                p.velocityX *= velScalarX
                                p.velocityY *= velScalarY
                                p.velocityX += accx*ts
                                p.velocityY += accy*ts
                                

                            elif option == 3:
                                dist = g.distance2(p.x, p.y, other.x, other.y)
                                dx = (dist[0]/dist[2])
                                dy = (dist[1]/dist[2])
                                p.velocityX = -p.velocityX*dx/2
                                p.velocityY = -p.velocityY*dy/2
                                other.velocityX = -p.velocityX*dx/2
                                other.velocityY = -p.velocityY*dy/2
                                while collission:
                                    p.x += p.velocityX * ts*10
                                    p.y += p.velocityY * ts*10
                                    other.x += other.velocityX * ts
                                    other.y += other.velocityY * ts
                                    dist = g.distance2(p.x, p.y, other.x, other.y)
                                    collission = dist[2] < (p.radius + other.radius)
                                


                            
                            #amountx = dist[0]/dist[2]
                            #amounty = dist[1]/dist[2]
                            #p.velocityX -= (collissionEnergy*amountx)/p.mass
                            #p.velocityY -= (collissionEnergy*amounty)/p.mass
                            #other.velocityX += (collissionEnergy*amountx)/other.mass
                            #other.velocityY += (collissionEnergy*amounty)/other.mass
                            #p.velocityX*=-amountx
                            #p.velocityY*=-amounty
                            #other.velocityX*=-amountx
                            #other.velocityY*=-amounty
        
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
            p.prevX = p.x
            p.prevY = p.y
            p.x += p.velocityX * ts
            p.y += p.velocityY * ts


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

