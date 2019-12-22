import re
from math import ceil


def produce(orders, recipies, supply):
    order = orders.pop(0)
    ammount = order[0]
    chem = order[1]

    if chem == 'ORE':
        supply['ORE'] += ammount
        return

    if ammount <= supply[chem]:
        supply[chem] -= ammount
        return

    ammount_needed = ammount - supply[chem]    
    reactions_needed = ceil(ammount_needed / recipies[chem][0])

    for ingredient in recipies[chem][1]:
        orders.append((ingredient[0] * reactions_needed, ingredient[1]))
        produce(orders, recipies, supply)

    supply[chem] += reactions_needed * recipies[chem][0] - ammount


if __name__ == '__main__':

    ruleRe = re.compile("(\d+) (\w+)")
    recipies = dict()
    supply = {'ORE': 0}
    with open('day14.txt') as f:
        for line in f.readlines():
            rule = line.split('=>')
            
            ingredients = [ruleRe.match(r.strip()).groups() for r in rule[0].strip().split(",")]
            chem = ruleRe.match(rule[1].strip()).groups()
            
            recipies[chem[1]] = (int(chem[0]), [(int(x[0]), x[1]) for x in ingredients])
            supply[chem[1]] = 0

    # Part 1
    orders = [(1, 'FUEL')]
    produce(orders, recipies, supply)
    print(supply['ORE'])

    # Part 2
    min_fuel, max_fuel = 0, 1e8
    while (max_fuel - min_fuel) > 1:
        m = (max_fuel + min_fuel) // 2

        orders = [(m, 'FUEL')]
        supply = {c: 0 for c in supply.keys()}
        produce(orders, recipies, supply)
        ore = supply['ORE']
        
        if ore > 1e12:
            max_fuel = m
        else:
            min_fuel = m

    print(min_fuel)
    