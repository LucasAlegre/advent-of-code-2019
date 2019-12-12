import re
from math import gcd


def lcm(a, b):
    return (a*b)//gcd(a, b)


class Moon:

    def __init__(self, x, y, z):
        self.x, self.y, self.z = x, y, z
        self.vx, self.vy, self.vz = 0, 0, 0
    
    def apply_velocity(self):
        self.x += self.vx
        self.y += self.vy 
        self.z += self.vz

    def compute_velocity(self, moons):
        for moon in moons:
            if self.x < moon.x:
                self.vx += 1
            elif self.x > moon.x:
                self.vx -= 1
            if self.y < moon.y:
                self.vy += 1
            elif self.y > moon.y:
                self.vy -= 1
            if self.z < moon.z:
                self.vz += 1
            elif self.z > moon.z:
                self.vz -= 1
    
    def total_energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vx) + abs(self.vy) + abs(self.vz))

    def __str__(self):
        return "pos=<x={}, y={}, z={}>, vel=<x={}, y={}, z={}>".format(self.x, self.y, self.z, self.vx, self.vy, self.vz)


if __name__ == '__main__':

    moons = []
    with open('day12.txt') as f:
        for line in f.readlines():
            x = re.match(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line.strip())
            moons.append(Moon(int(x.group(1)), int(x.group(2)), int(x.group(3))))
    
    # Part 1
    """ for i in range(1, 1000+1):
        for moon in moons:
            moon.compute_velocity(moons)
        for moon in moons:
            moon.apply_velocity()
    print(sum([moon.total_energy() for moon in moons])) """

    #Part 2
    x_rep, y_rep, z_rep = -1, -1, -1
    xi = tuple(m.x for m in moons)
    yi = tuple(m.y for m in moons)
    zi = tuple(m.z for m in moons)
    for i in range(1, 10000000):
        for moon in moons:
            moon.compute_velocity(moons)
        for moon in moons:
            moon.apply_velocity()

        xs = tuple(m.x for m in moons)
        ys = tuple(m.y for m in moons)
        zs = tuple(m.z for m in moons)
        if xs == xi:
            x_rep = i+1 if x_rep == -1 else x_rep
        if ys == yi:
            y_rep = i+1 if y_rep == -1 else y_rep
        if zs == zi:
            z_rep = i+1 if z_rep == -1 else z_rep
        
        if x_rep != -1 and y_rep != -1 and z_rep != -1:
            break
    
    print(lcm(lcm(x_rep, y_rep), z_rep))
        

