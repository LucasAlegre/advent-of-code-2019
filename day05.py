class Computer:

    def __init__(self, prog):
        self.prog = prog

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

    def run(self):
        ip = 0
        while self.prog[ip] != 99:
            opcode, mode1, mode2 = self.parse_instruction(self.prog[ip])

            if opcode == 1:
                op1, op2, op3 = self.prog[ip+1], self.prog[ip+2], self.prog[ip+3]
                self.prog[op3] = self.read_value(op1, mode1) + self.read_value(op2, mode2)
                ip += 4

            elif opcode == 2:
                op1, op2, op3 = self.prog[ip+1], self.prog[ip+2], self.prog[ip+3]
                self.prog[op3] = self.read_value(op1, mode1) * self.read_value(op2, mode2)
                ip += 4
            
            elif opcode == 3:
                self.prog[self.prog[ip+1]] = int(input("Input: "))
                ip += 2

            elif opcode == 4:
                op1 = self.read_value(self.prog[ip+1], mode1)
                print("Ouput:", op1)
                ip += 2
            
            elif opcode == 5:
                op1, op2 = self.prog[ip+1], self.prog[ip+2]
                if self.read_value(op1, mode1) != 0:
                    ip = self.read_value(op2, mode2)
                else:
                    ip += 3
            
            elif opcode == 6:
                op1, op2 = self.prog[ip+1], self.prog[ip+2]
                if self.read_value(op1, mode1) == 0:
                    ip = self.read_value(op2, mode2)
                else:
                    ip += 3
            
            elif opcode == 7:
                op1, op2, op3 = self.prog[ip+1], self.prog[ip+2], self.prog[ip+3]
                if self.read_value(op1, mode1) < self.read_value(op2, mode2):
                    self.prog[op3] = 1
                else:
                    self.prog[op3] = 0
                ip += 4

            elif opcode == 8:
                op1, op2, op3 = self.prog[ip+1], self.prog[ip+2], self.prog[ip+3]
                if self.read_value(op1, mode1) == self.read_value(op2, mode2):
                    self.prog[op3] = 1
                else:
                    self.prog[op3] = 0
                ip += 4


if __name__ == '__main__':

    with open('day05.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')]
    
    computer = Computer(prog_input)
    computer.run()