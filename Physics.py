import Geometry as g
import math, time

G = 6.67*10**-11


class PointMass2():
    def __init__(self, mass, x, y, velocityX, velocityY):
        self.x = x
        self.y = y
        self.mass = mass
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.prevX = x
        self.prevY = y
        self.nextX = x
        self.nextY = y
        self.color = (200, 200, 200)

    def getVelocity(self):
        v = g.distance2(0, 0, self.velocityX, self.velocityY)
        return v

    def getRadius(self):
        return math.pow(self.mass*4/3*math.pi, 1/2)


class PointMass3(g.Point3):
    # inherits position
    def __init__(self, mass, x, y, z, velocityX, velocityY, velocityZ):
        super().__init__(x, y, z)
        self.mass = mass
        self.velocityX = velocityX
        self.velocityY = velocityY
        self.velocityZ = velocityZ

    def velocity(self):
        v = g.distance3(0, 0, 0, self.velocityX,
                        self.velocityY, self.velocityZ)
        return v


class World2:
    def __init__(self, lop: list()):
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
                if p.y-p.getRadius() < 0:
                    p.y = 0+p.getRadius()
                    p.velocityY *= -(1)
                elif p.y+p.getRadius() > H:
                    p.y = H-p.getRadius()
                    p.velocityY *= -(1)
                if p.x-p.getRadius() < 0:
                    p.x = 0+p.getRadius()
                    p.velocityX *= -(1)
                elif p.x+p.getRadius() > W:
                    p.x = W-p.getRadius()
                    p.velocityX *= -(1)

        if settings["bodyCollissions"]:
            for p in self.pointsList:
                for other in self.pointsList:
                    if p != other:
                        dist = g.distance2(p.x, p.y, other.x, other.y)
                        collission = dist[2] < (
                            p.getRadius() + other.getRadius())
                        if collission:
                            # dist[2]**2 potentially
                            repAcc = -(G*p.mass*other.mass) / (dist[2]**1.8) / p.mass
                            p.velocityX += repAcc*(dist[0]/dist[2])*ts
                            p.velocityY += repAcc*(dist[1]/dist[2])*ts

        if settings["merging"]:
            for p in self.pointsList:
                for other in self.pointsList:
                    if p != other:
                        dist = g.distance2(p.x, p.y, other.x, other.y)
                        if dist[2] < p.getRadius():
                            p.mass += other.mass
                            resvx = p.velocityX + other.velocityX
                            resvy = p.velocityY + other.velocityY
                            p.velocityX = resvx*(p.mass/(p.mass+other.mass))
                            p.velocityY = resvy*(p.mass/(p.mass+other.mass))
                            self.pointsList.remove(other)
                            print("merge uwu")
        t1 = time.time()
        if settings["nbody"]:
            for p in self.pointsList:
                for other in self.pointsList:
                    if p != other:
                        #newVel = newVelDue2(p, other, ts)
                        newVel = newVelDueOther2(p, other, ts)
                        p.velocityX = newVel[0]
                        p.velocityY = newVel[1]
        timetaken = time.time()-t1
        # this runs at the end regardless of which you choose, since al lthe functions only update the velocity
        for p in self.pointsList:
            Cd = 100
            speedX = abs(p.velocityX)
            speedY = abs(p.velocityY)
            dragX = (Cd*speedX**2/2)*g.sign(p.velocityX)
            dragY = (Cd*speedY**2/2)*g.sign(p.velocityY)
            p.velocityX -= dragX*0
            p.velocityY -= dragY*0
            p.x += p.velocityX * ts
            p.y += p.velocityY * ts


def forceDue2(p: PointMass2, other: PointMass2):
    dist = g.distance2(p.x, p.y, other.x, other.y)
    resForce = (G * p.mass * other.mass)/dist[2]**2
    return resForce


def accDue2(p: PointMass2, other: PointMass2):
    f = forceDue2(p, other)
    dist = g.distance2(p.x, p.y, other.x, other.y)
    a = f/p.mass
    ax = a*(dist[0]/dist[2])
    ay = a*(dist[1]/dist[2])
    return [ax, ay, a]


def newVelDue2(p: PointMass2, other: PointMass2, ts):
    accXYC = accDue2(p, other)
    velX = accXYC[0]*ts
    velY = accXYC[1]*ts
    return [p.velocityX+velX, p.velocityY+velY]

def newVelDueOther2(p: PointMass2, other: PointMass2, ts):
    #this is a summary of the other functions into one, to avoid duplicated calculations
    dist = g.distance2(p.x, p.y, other.x, other.y)
    resForce = (G * p.mass * other.mass)/dist[2]**2
    a = resForce/p.mass
    ax = a*(dist[0]/dist[2])
    ay = a*(dist[1]/dist[2])
    
    velX = ax*ts
    velY = ay*ts
    return [p.velocityX+velX, p.velocityY+velY]

def dispDue2(p: PointMass2, other: PointMass2, ts):
    acc = accDue2(p, other)
    dispX = p.velocityX + 0.5*acc[0]*ts**2
    dispY = p.velocityY + 0.5*acc[1]*ts**2
    return [dispX, dispY]


def newPosDue2(p: PointMass2, other: PointMass2, ts):
    disp = dispDue2(p, other, ts)
    newX = p.x+disp[0]
    newY = p.y+disp[1]
    return [newX, newY]
