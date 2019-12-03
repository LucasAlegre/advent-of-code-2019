def manhattan(c):
    return abs(c[0]) + abs(c[1])


if __name__ == '__main__':

    with open('day03.txt') as f:
        paths = [path.strip() for path in f.readlines()]  
        paths = [p.split(',') for p in paths]

    distances = []
    for path in paths:
        x, y = 0, 0
        steps = 0
        d = dict()
        for p in path:
            direction, distance = p[0], int(p[1:])
            if direction == 'U':
                for i in range(1, distance+1):
                    steps += 1
                    if (x,y+i) not in d:
                        d[(x,y+i)] = steps
                x, y = x, y + distance
            elif direction == 'D':
                for i in range(1, distance+1):
                    steps += 1
                    if (x,y-i) not in d:
                        d[(x,y-i)] = steps
                x, y = x, y - distance
            elif direction == 'L':
                for i in range(1, distance+1):
                    steps += 1
                    if (x-i,y) not in d:
                        d[(x-i,y)] = steps
                x, y = x - distance, y
            elif direction == 'R':
                for i in range(1, distance+1):
                    steps += 1
                    if (x+i,y) not in d:
                        d[(x+i,y)] = steps
                x, y = x + distance,  y

        distances.append(d)

    coords = distances[0].keys() & distances[1].keys()

    # Part 1
    c = min(coords, key=manhattan)
    print(manhattan(c))

    # Part 2
    c = min(coords, key=lambda x: distances[0][x] + distances[1][x])
    print(distances[0][c] + distances[1][c])

        


    