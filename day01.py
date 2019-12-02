from math import floor


def mass_to_fuel(mass):
    return floor(mass/3) - 2


if __name__ == '__main__':

    with open('day01.txt') as f:
        mass = [int(x) for x in f.readlines()]

    # Part1: 
    # print(sum(map(mass_to_fuel, mass)))

    # Part 2:
    c = 0
    for m in mass:
        while m > 0:
            m = max(0, mass_to_fuel(m))
            c += m
    print(c)
