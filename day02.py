from itertools import permutations


def run_program(noun, verb, prog):
    prog[1] = noun
    prog[2] = verb

    ip = 0
    while prog[ip] != 99:
        if prog[ip] == 1:
            prog[prog[ip+3]] = prog[prog[ip+1]] + prog[prog[ip+2]]

        elif prog[ip] == 2:
            prog[prog[ip+3]] = prog[prog[ip+1]] * prog[prog[ip+2]]
        
        ip += 4

    return prog[0]


if __name__ == '__main__':

    with open('day02.txt') as f:
        prog_input = [int(x) for x in f.read().split(',')]

    for noun, verb in permutations(range(100), 2):
        prog = prog_input.copy()
        
        if run_program(noun, verb, prog) == 19690720:
            print(100 * noun + verb)
            break