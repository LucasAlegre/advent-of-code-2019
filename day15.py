from collections import deque
import time


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

    def run_step(self, inp):
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
                self.prog[self.read_write_address(op1, mode1)] = inp

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

    with open('day13.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')] + [0 for i in range(100000)]
    
    computer = Computer(prog_input)

    ended = False
    width = 40
    height = 40
    display = []
    for _ in range(height):
        display.append([' ' for _ in range(width)])

    x, y = 0, 0
    while not ended:
        inp = int(input())
        output = computer.run_step(inp)
        if 

        for row in range(height):
            print(' '.join(display[row]))