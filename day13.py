from collections import deque
import time

def sign(x):
    if x < 0:
        return -1
    if x == 0:
        return 0
    else:
        return 1

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

    def run_step(self, padposX, ballposX):
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
                self.prog[self.read_write_address(op1, mode1)] = -sign(padposX - ballposX) #key_to_int(input())

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

def tile_to_str(tile_id):
    if tile_id == 0:
        return ' '
    elif tile_id == 4:
        return '\u25CF'
    elif tile_id == 2:
        return '\u2591'
    elif tile_id == 1:
        return '\u2588'
    elif tile_id == 3:
        return '\u2501'

def key_to_int(key):
    if key == '\x1b[D':
        return -1
    elif key == '\x1b[C':
        return 1
    elif key == '\x1b[B':
        return 0

if __name__ == '__main__':

    with open('day13.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')] + [0 for i in range(100000)]

    # Part 1
    """computer = Computer(prog_input)
    screen = {}
    while not computer.is_halt():
        x = computer.run_step()
        y = computer.run_step()
        tile_id = computer.run_step()

        screen[(x,y)] = tile_id
    print(list(screen.values()).count(2)) """

    # Part 2
    prog_input[0] = 2
    computer = Computer(prog_input)

    width = 40
    height = 22
    score = 0
    display = []
    padposX, ballposX = 0, 0
    for _ in range(height):
        display.append([' ' for _ in range(width)])

    while not computer.is_halt():
        if computer.prog[computer.ip] == 99:
            computer.ip = 0

        x = computer.run_step(padposX, ballposX)
        y = computer.run_step(padposX, ballposX)
        
        if x == -1 and y == 0:
            score = computer.run_step(padposX, ballposX)
            print('Score:', score)
        else:
            tile_id = computer.run_step(padposX, ballposX)
            display[y][x] = tile_to_str(tile_id)
            if tile_id == 3:
                padposX = x
            elif tile_id == 4:
                ballposX = x
    
        for row in range(height):
            print(' '.join(display[row]))
        #time.sleep(0.01)
    
    print(score)

