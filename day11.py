from collections import deque


class Computer:

    def __init__(self, prog=None):
        self.prog = prog
        self.ip = 0
        self.base = 0

    def parse_instruction(self, i):
        i = str(i)
        opcode = int(i[-1])
        mode1 = int(i[-3]) if len(i) > 2 else 0
        mode2 = int(i[-4]) if len(i) > 3 else 0
        mode3 = int(i[-5]) if len(i) > 4 else 0

        return opcode, mode1, mode2, mode3

    def read_value(self, op, mode):
        if mode == 0:
            return self.prog[op]
        elif mode == 1:
            return op
        elif mode == 2:
            return self.prog[self.base + op]
    
    def read_write_address(self, op, mode):
        if mode == 2:
            return op + self.base
        else:
            return op

    def is_halt(self):
        return self.prog[self.ip] == 99

    def run_step(self, color):
        while self.prog[self.ip] != 99:
            opcode, mode1, mode2, mode3 = self.parse_instruction(self.prog[self.ip])
            
            if opcode == 1:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                self.prog[self.read_write_address(op3, mode3)] = self.read_value(op1, mode1) + self.read_value(op2, mode2)
                self.ip += 4

            elif opcode == 2:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                self.prog[self.read_write_address(op3, mode3)] = self.read_value(op1, mode1) * self.read_value(op2, mode2)
                self.ip += 4
            
            elif opcode == 3:
                op1 = self.prog[self.ip+1]
                self.prog[self.read_write_address(op1, mode1)] = color

                self.ip += 2

            elif opcode == 4:
                op1 = self.read_value(self.prog[self.ip+1], mode1)
                self.ip += 2
                return op1
            
            elif opcode == 5:
                op1, op2 = self.prog[self.ip+1], self.prog[self.ip+2]
                if self.read_value(op1, mode1) != 0:
                    self.ip = self.read_value(op2, mode2)
                else:
                    self.ip += 3
            
            elif opcode == 6:
                op1, op2 = self.prog[self.ip+1], self.prog[self.ip+2]
                if self.read_value(op1, mode1) == 0:
                    self.ip = self.read_value(op2, mode2)
                else:
                    self.ip += 3
            
            elif opcode == 7:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                if self.read_value(op1, mode1) < self.read_value(op2, mode2):
                    self.prog[self.read_write_address(op3, mode3)] = 1
                else:
                    self.prog[self.read_write_address(op3, mode3)] = 0
                self.ip += 4

            elif opcode == 8:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                if self.read_value(op1, mode1) == self.read_value(op2, mode2):
                    self.prog[self.read_write_address(op3, mode3)] = 1
                else:
                    self.prog[self.read_write_address(op3, mode3)] = 0
                self.ip += 4
            
            elif opcode == 9:
                op1 = self.read_value(self.prog[self.ip+1], mode1)
                self.base += op1
                self.ip += 2


if __name__ == '__main__':

    with open('day11.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')] + [0 for i in range(100000)]

    computer = Computer(prog_input)

    # Part 1
    """ 
    coord = (0,0)
    direction = deque([(0,1), (1,0), (0,-1), (-1,0)])
    color = 0
    grid = {(0,0): 0}
    painted_panels = set()
    while not computer.is_halt():
        paint_color = computer.run_step(color)

        if computer.run_step(color) == 0:
            direction.rotate(1)
        else:
            direction.rotate(-1)

        grid[coord] = paint_color
        painted_panels.add(coord)

        coord = (coord[0] + direction[0][0], coord[1] + direction[0][1])
        color = grid[coord] if coord in grid else 0 
    print(len(painted_panels)) """

    # Part2
    coord = (0,0)
    direction = deque([(0,1), (1,0), (0,-1), (-1,0)])
    color = 1
    grid = {(0,0): 1}
    while not computer.is_halt():
        paint_color = computer.run_step(color)

        if computer.run_step(color) == 0:
            direction.rotate(1)
        else:
            direction.rotate(-1)

        grid[coord] = paint_color

        coord = (coord[0] + direction[0][0], coord[1] + direction[0][1])
        color = grid[coord] if coord in grid else 0 
    
    coords = grid.keys()
    maxx = max([c[0] for c in coords]) 
    minx = min([c[0] for c in coords])
    maxy = max([c[1] for c in coords]) 
    miny = min([c[1] for c in coords])
    width = maxx - minx + 1
    height = maxy - miny + 1

    paint = []
    for _ in range(height):
        paint.append([' ' for _ in range(width)])
    
    for c in grid.keys():
        if grid[c] == 1:
            x = c[0] - minx
            y = c[1] - miny
            paint[height - y -1][x] = '\u2588'
    
    for row in range(height):
        print(''.join(paint[row]))

