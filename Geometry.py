import numpy as np
import math
import time

class Point2:
    # a 2D point
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Point3:
    #a 3D point
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

def distance2(x1,y1, x2,y2):
    #returns the distance between two points in 2D space
    dist = np.sqrt(np.power((x2-x1), 2) + np.power((y2-y1), 2))
    dx = x2-x1
    dy = y2-y1
    return [dist, dx, dy]
def distance2b(dx,dy):
    #returns the distance between two points in 2D space
    dist = np.sqrt(np.power(dx, 2) + np.power(dy, 2))
    return dist

def distance2XY(p1, p2):
    #returns the x, y components of positonal difference
    return [p2.x-p1.x, p2.y-p1.y]

def distance3(x1, y1, z1, x2, y2, z2):
    #returns the distance between two points in 3D space
    return np.sqrt(np.power((x2-x1), 2) + np.power((y2-y1), 2) + np.power((z2-z1), 2))

def distance3XY(x1, y1, z1, x2, y2, z2):
    #returns the x, y, z components of positonal difference
    dx = x2-x1
    dy = y2-y1
    dz = z2-z1
    return [dx, dy, dz]

def deltaAngle2(p1:Point2, p2:Point2, p3:Point2):
    #Gives the angle between p2,p1 and p2,p3.
    #use on the last three coordinates in the movement history for example to get change of angle
    a=[p2.x-p1.x, p2.y-p1.y]
    b=[p2.x-p3.x, p2.y-p3.y]
    magA=distance2(p2.x, p2.y, p1.x, p1.y)
    magB=distance2(p2.x, p2.y, p3.x, p3.y)
    abDot=np.dot(a,b)
    #abDot= a[0]*b[0]+a[1]*b[1]
    theta = math.acos(abDot/(magA*magB))
    return np.rad2deg(theta)

def deltaAngle3(p1:Point3, p2:Point3, p3:Point3):
    #same as deltaAngle2, but in 3D
    a=[p2.x-p1.x, p2.y-p1.y, p2.z-p1.z]
    b=[p2.x-p3.x, p2.y-p3.y, p2.z-p3.z]
    magA=distance3(p2.x, p2.y, p2.z, p1.x, p1.y, p1.z)
    magB=distance3(p2.x, p2.y, p2.z, p3.x, p3.y, p3.z)
    abDot=np.dot(a,b)
    theta = math.acos(abDot/(magA*magB))
    return np.rad2deg(theta)

def triangleAreaHeron(p1, p2, p3):
    #this uses Heron's formula for the area of a triangle which apparantly(?) is not always exact 
    a=distance2(p1.x, p1.y, p2.x, p2.y)
    b=distance2(p2.x, p2.y, p3.x, p3.y)
    c=distance2(p3.x, p3.y, p1.x, p1.y)
    s=(a+b+c)/2
    A=np.sqrt(s*(s-a)*(s-b)*(s-c))
    return A
def triangleAreaHeron_Nonumpy_withfunctions(p1, p2, p3):
    #this uses Heron's formula for the area of a triangle which apparantly(?) is not always exact 
    a=distance2NN(p2.x,p2.y,p1.x,p1.y)
    b=distance2NN(p2.x,p2.y,p3.x,p3.y)
    c=distance2NN(p3.x,p3.y,p1.x,p1.y)
    s=(a+b+c)/2
    A=np.sqrt(s*(s-a)*(s-b)*(s-c))
    return A
def triangleAreaHeron_Nonumpy_nofunctions(p1, p2, p3):
    #this uses Heron's formula for the area of a triangle which apparantly(?) is not always exact 
    a=math.sqrt((p2.x-p1.x)**2 + (p2.y-p1.y)**2)
    b=math.sqrt((p2.x-p3.x)**2 + (p2.y-p3.y)**2)
    c=math.sqrt((p3.x-p1.x)**2 + (p3.y-p1.y)**2)
    s=(a+b+c)/2
    A=np.sqrt(s*(s-a)*(s-b)*(s-c))
    return A

def triangleAreaBluu(p1, p2, p3):
    Ax=p1.x
    Ay=p1.y
    Bx=p2.x-Ax
    By=p2.y-Ay
    Cx=p3.x-Ax
    Cy=p3.y-Ay
    t1=Cx - (Cy * By**2 * Bx + Bx**2 * Cx * By)/(By**3 + By * Bx**2)
    t2=Cy - (Cx * Bx**2 * By + By**2 * Cy * Bx)/(Bx * By**2 + Bx**3)

    #H=np.sqrt(t1**2 + t2**2)
    H=math.sqrt(t1**2+t2**2)
    B=math.sqrt((Bx-Ax)**2 + (By-Ay)**2)

    #B=distance2(Ax,Ay,Bx,By)
    return (B*H)/2

def triangleAreaDot(p1, p2, p3):
    pass

def sign(n):
    if n<0:
        return -1
    elif n>=0:
        return 1

if False:
        
    p1=Point2(0,0)
    p2=Point2(6,2)
    p3=Point2(3,4)

    print(triangleAreaBluu(p1, p2, p3))
    print(triangleAreaHeron(p1, p2, p3))

    iterations = 1000000
    t1A = time.time()
    for n in range(iterations):
        triangleAreaHeron(p1, p2, p3)
    dt1=time.time()-t1A
    print("time for 1e6 heron: ", dt1)

    t1B = time.time()
    for n in range(iterations):
        triangleAreaBluu(p1, p2 , p3)
    dt2=time.time()-t1B
    print("time for 1e6 bluu:  ", dt2)

    print("Bluu is ", int(100*(dt1/dt2-1)), "% faster")