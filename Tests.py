import unittest
import Geometry as g
import numpy as np
import time

a=g.Point2(-2,-1)
b=g.Point2(0,1)
c=g.Point2(2,-1)
#makes a triangle symmetrically over the middle of the zero line, /_\, testing the angle at the middle point

d=g.Point3(-1, -2, -3)
e=g.Point3(0, 0, 0)
f=g.Point3(4, 5, 6)
#a 3D point "behind" the 0,0 orgin

class testGeometryLib(unittest.TestCase):
    # lines/vectors with orgin at 0,0, at 45 deg in a circle

    def test_distance2(self):
        self.assertAlmostEqual(a.distance2(b), np.sqrt(2)*2)
        self.assertAlmostEqual(b.distance2(c), np.sqrt(2)*2)
        self.assertAlmostEqual(c.distance2(a), 4)

    def test_distance2XY(self):
        self.assertEqual(a.distance2XY(b), [2,2])
        self.assertEqual(b.distance2XY(c), [2,-2])
        self.assertEqual(c.distance2XY(a), [-4,0])
        self.assertEqual(a.distance2XY(c), [4,0])
    
    def test_distance3(self):
        pass
    
    def test_distance3XY(self):
        l1 = g.distance3XY(e.x, e.y, e.z, d.x, d.y, d.z)
        l2 = g.distance3XY(e.x, e.y, e.z, f.x, f.y, f.z)
        l3 = g.distance3XY(f.x, f.y, f.z, d.x, d.y, d.z)
        l4 = g.distance3XY(d.x, d.y, d.z, f.x, f.y, f.z)
        self.assertEqual(l1, [-1, -2, -3])
        self.assertEqual(l2, [4, 5, 6])
        self.assertEqual(l3, [-5, -7, -9])
        self.assertEqual(l4, [5, 7, 9])
    
    def test_deltaAngle2(self):
        self.assertAlmostEqual(g.deltaAngle2(a, b, c), 90, 5)        
        self.assertAlmostEqual(g.deltaAngle2(b, c, a), 45, 5)
        self.assertAlmostEqual(g.deltaAngle2(c, a, b), 45, 5)

    def test_deltaAngle3(self):
        self.assertAlmostEqual(g.deltaAngle3(d, e, f), 167.067, 3)
    
    def perfTriangleArea(self):
        target=2.83024341317
        p1=g.Point2(0,0)
        p2=g.Point2(6,2)
        p3=g.Point2(3,4)
        self.assertAlmostEqual(g.triangleAreaHeron(p1, p2, p3), target)
        self.assertAlmostEqual(g.triangleAreaBluu(p1, p2, p3), target)

        t1A = time.time()
        for n in range(1e6):
            g.triangleAreaHeron(p1, p2, p3)
        dt=time.time()-t1A
        print("time for 1e6 heron: ", dt)
        
        t1B = time.time()
        for n in range(1e6):
            g.triangleAreaBluu(p1, p2 , p3)
        dt=time.time()-t1B
        print("time for 1e6 bluu: ", dt)


if __name__=='main':
    unittest.main

# python -m unittest Tests.testGeometryLib