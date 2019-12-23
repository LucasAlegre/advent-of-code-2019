from collections import deque
import time
from copy import deepcopy


class Computer:

    def __init__(self, prog=None):
        self.prog = prog
        self.ip = 0
        self.base = 0
    
    def __deepcopy__(self, memo):
        c = Computer()
        c.prog = deepcopy(self.prog)
        c.ip = self.ip
        c.base = self.base
        return c

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

    def run_step(self, inp=None):
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
                self.prog[self.read_write_address(op1, mode1)] = inp.pop(0)

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

def get_intersections(view):
    num_rows = len(view)
    num_columns = len(view[0])
    d = [(0,1), (1,0), (0,-1), (-1,0)]
    intersections = []
    for i in range(1, num_rows-1):
        for j in range(1, num_columns-1):
            intersection = True
            if view[i][j] == '#':
                for m in d:
                    if view[i+m[0]][j+m[1]] != '#':
                        intersection = False
            else:
                intersection = False
            if intersection:
                intersections.append((i,j))
    return intersections

if __name__ == '__main__':

    with open('day17.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')] + [0 for i in range(10000)]

    # Part 1
    computer = Computer(prog_input.copy())
    view = []
    line = ''
    while not computer.is_halt():
        output = computer.run_step()
        if output is None:
            break
        if output == 10:
            if line != '':
                view.append(line)
                line = ''
        else:
            line += chr(output)
        
    print(sum([x[0]*x[1] for x in get_intersections(view)]))
    for line in view:
        print(line, len(line))

    # Part 2
    A = 65
    B = 66
    C = 67
    COMMA = 44
    NEWLINE = 10
    L = 76
    R = 82
    main_routine = [65, 44, 66, 44, 67, 44, 66, 44, 65, 44, 67, 10]
    func_A = [L, COMMA, ord('4'), COMMA, L, COMMA, ord('8'), NEWLINE]
    func_B = [82, 44, 52, 44, 82, 44, 52, 44, 82, 44, 56, 10]
    func_C = [76, 44, 54, 44, 76, 44, 50, 10]
    inputs = main_routine + func_A + func_B + func_C + [ord('y'), NEWLINE]

    prog_input[0] = 2
    computer = Computer(prog_input)

    while inputs:
        a = computer.run_step(inputs)
        #print(a, inputs)

    view = []
    line = ''
    while not computer.is_halt():
        output = computer.run_step()
        if output is None:
            for line in view:
                print(line, len(line))
            break
        if output == 10:
            if line != '':
                view.append(line)
                line = ''
        else:
            line += chr(output)
