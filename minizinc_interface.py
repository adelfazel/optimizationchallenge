from minizinc import Instance, Model, Solver
from functools import reduce


class minizincSolver:
    def __init__(self, items, capacity):
        self.items = sorted(items, key=lambda x: x.value / x.weight)
        self.num_items = len(items)
        self.model = Model()
        self.capacity = capacity
        self.best_solution = []


    def get_initial_solution(self):
        used_capacity = 0
        solution = []
        itemSelectionIndex = 0
        while used_capacity + self.items[itemSelectionIndex].weight <= self.capacity:
            solution.append(self.items[itemSelectionIndex].index)
            used_capacity += self.items[itemSelectionIndex].weight
            itemSelectionIndex += 1
        self.best_solution = solution
        return solution

    def get_value_from_solution(self, solution):
        filter(lambda x:solution,map(lambda x:x.value,self.items))
        return reduce(lambda e1, e2: e1.value + e2.value, )

    def create_minizinc_model(self):
        capacity = f"int: capacity={self.capacity};\n"
        items = f"set of int: Items=1..{self.num_items};\n"
        weights = f"array[Items] of int: weights={[item.weight for item in self.items]};\n"
        values = f"array[Items] of int: values={[item.value for item in self.items]};\n"
        decision_variables = f"array[Items] of var 0..1: picks;\n"
        capacity_constraint = "var 0..capacity: remaining_cap=capacity-sum(i in Items)(picks[i]*weights[i]);\n"
        obj = f"var int:obj=sum(i in Items)(picks[i]*values[i]);\n"
        self.add_string_to_model(items)
        self.add_string_to_model(capacity)
        self.add_string_to_model(weights)
        self.add_string_to_model(values)
        self.add_string_to_model(decision_variables)
        self.add_string_to_model(capacity_constraint)
        self.add_string_to_model(obj)
        self.add_string_to_model("""solve satisfy;\n""")

    def add_string_to_model(self, content):
        self.model.add_string(content)

    def get_objective(self):
        return self.get_solution().objective

    def get_taken_items(self):
        return [self.get_solution().picks[self.items[i].index] for i in range(len(self.items))]

    def set_result(self, result):
        self.result = result

    def setup(self):
        gecode = Solver.lookup("or-tools")
        self.instance = Instance(gecode, self.model)

    def add_new_obj(self, obj):
        self.add_string_to_model(f"constraint obj>{obj}\n")

    def solve(self):
        self.set_result(self.instance.solve())

    def get_solution(self):
        return self.result.solution

    def get_best_solution(self):
        return
