#!/usr/bin/python
# -*- coding: utf-8 -*-
from minizinc_interface import minizincSolver
from collections import namedtuple

Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    lines = input_data.split('\n')
    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))
    items = sorted(items,key=lambda x:x.value/x.weight)
    solver = minizincSolver(items, capacity)
    solver.create_minizinc_model()
    solver.setup()
    solver.add_new_obj(solver.get_value_from_solution(solver.get_initial_solution()))
    solver.solve()
    value = solver.get_objective()
    taken = solver.get_taken_items()
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
