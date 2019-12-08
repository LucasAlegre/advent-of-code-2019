from itertools import permutations

input_buffer = []

class Computer:

    def __init__(self, prog=None):
        self.prog = prog
        self.ip = 0

    def parse_instruction(self, i):
        i = str(i)
        opcode = int(i[-1])
        mode1 = int(i[-3]) if len(i) > 2 else 0
        mode2 = int(i[-4]) if len(i) > 3 else 0

        return opcode, mode1, mode2

    def read_value(self, op, mode):
        if mode == 0:
            return self.prog[op]
        elif mode == 1:
            return op

    def is_halt(self):
        return self.prog[self.ip] == 99

    def run(self, prog=None, reset_ip=True):
        if reset_ip:
            self.ip = 0
        if prog is not None:
            self.prog = prog
        
        while self.prog[self.ip] != 99:
            opcode, mode1, mode2 = self.parse_instruction(self.prog[self.ip])
            
            if opcode == 1:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                self.prog[op3] = self.read_value(op1, mode1) + self.read_value(op2, mode2)
                self.ip += 4

            elif opcode == 2:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                self.prog[op3] = self.read_value(op1, mode1) * self.read_value(op2, mode2)
                self.ip += 4
            
            elif opcode == 3:
                self.prog[self.prog[self.ip+1]] = input_buffer.pop(0)
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
                    self.prog[op3] = 1
                else:
                    self.prog[op3] = 0
                self.ip += 4

            elif opcode == 8:
                op1, op2, op3 = self.prog[self.ip+1], self.prog[self.ip+2], self.prog[self.ip+3]
                if self.read_value(op1, mode1) == self.read_value(op2, mode2):
                    self.prog[op3] = 1
                else:
                    self.prog[op3] = 0
                self.ip += 4


if __name__ == '__main__':

    with open('day07.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')]
    
    # Part 1
    """ amps = [Computer() for _ in range(5)]
    max_output = 0
    for a in permutations(range(5), 5):
        phase = list(a)
        output = 0
        for amp in amps:
            input_buffer.append(phase.pop(0))
            input_buffer.append(output)
            output = amp.run(prog_input.copy())
        max_output = max(max_output, output)

    print(max_output)   """  
    
    # Part 2
    max_output = 0
    for a in permutations(range(5, 10), 5):
        amps = [Computer(prog_input.copy()) for _ in range(5)]
        phase = list(a)
        output = 0
        first = True
        while not amps[0].is_halt():
            for amp in amps:
                if first:
                    input_buffer.append(phase.pop(0))
                input_buffer.append(output)
                output = amp.run(reset_ip=False)
            first = False
            if output is not None:
                max_output = max(max_output, output)

    print(max_output)
