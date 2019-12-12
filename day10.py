from math import atan2, pi


def angle(x0, y0, x1, y1):
    return atan2((y1-y0),(x1-x0))

def detection_number(x, y, m):
    angles = set()
    for x1 in range(len(m)):
        for y1 in range(len(m[0])):
            if (x1, y1) != (x, y) and m[x1][y1] == 1:
                angles.add(angle(x,y,x1,y1))
    return len(angles)

def create_sets(x, y, m):
    coords_angle = {}
    for x1 in range(len(m)):
        for y1 in range(len(m[0])):
            if (x1, y1) != (x, y) and m[x1][y1] == 1:
                a = angle(x,y,x1,y1)
                if a in coords_angle:
                    coords_angle[a].append((x1,y1))
                else:
                    coords_angle[a] = [(x1,y1)]
    for a in coords_angle:
        coords_angle[a].sort(key=lambda c: abs(c[0]-x) + abs(c[1]-y))
    return coords_angle


if __name__ == '__main__':

    with open('day10.txt') as f:
        m = []
        for line in f.readlines():
            m.append([1 if c == '#' else 0 for c in line.strip()])

    # Part 1
    d = {}
    for x in range(len(m)):
        for y in range(len(m[0])):
            if m[x][y] == 1:
                d[(x,y)] = detection_number(x, y, m)
    coord = max(d, key=d.get)
    print(d[coord])

    # Part 2
    d = create_sets(coord[0], coord[1], m)
    sorted_angles = sorted(d.keys())[::-1]
    c = 1
    for a in sorted_angles:
        vaporized = d[a].pop(0)
        if c == 200:
            break
        c += 1
    print(vaporized[1]*100 + vaporized[0])
