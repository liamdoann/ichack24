import json
from typing import Any, Dict
from z3 import *

def build_constraints(json_data: Dict[str, Any]):
    constraints = []

    desks = json_data["desks"]
    students = json_data["students"]
    at_front = json_data["at_front"]
    keep_separate = json_data["keep_separate"]

    xs = [Int(f'{student}_x') for student in students]
    ys = [Int(f'{student}_y') for student in students]
    
    for i in range(len(students)):
        # Every student sits at a desk.
        constraints.append(Or(*[And(xs[i] == int(x), ys[i] == y) for x in desks.keys() for y in desks[x]]))

        # No two students sit in the same place.
        for j in range(len(students)):
            if i != j:
                constraints.append(Not(And(xs[i] == xs[j], ys[i] == ys[j])))

    # Students should be sat at the front are in the first row.
    for s in at_front:
        index = students.index(s)
        constraints.append(xs[index] == min(desks.keys()))

    # Students who should be kept separate do not sit adjacent to each other.
    for s1, others in keep_separate.items():
        for s2 in others:
            index1 = students.index(s1)
            index2 = students.index(s2)
            constraints.append((Abs(xs[index1] - xs[index2]) + Abs(ys[index1] - ys[index2])) != 1)
    
    return constraints, students

def solve(json_data: Dict[str, Any]):   
    constraints, students = build_constraints(json_data)

    solver = Solver()
    solver.add(constraints)

    if solver.check() == unsat:
        print("No plan possible.")
        return (False, None)
    else:
        m = solver.model()
        
        result = {}

        for x in m:
            name, coord = str(x).split("_")
            print(name, coord)
            if name in result:
                result[name][coord] = m[x]
            else:
                result[name] = {coord : m[x]}
        
        return (True, result)
    
def run(input_file):
    json_data: Dict[str, Any] = json.load(open(input_file))
    solve(json_data)