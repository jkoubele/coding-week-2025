from itertools import product, combinations

import graphviz
import numpy as np
import pandas as pd
import pulp
from faker import Faker
from pulp import LpProblem, LpVariable, LpMaximize, lpSum


def sanitize_name(name: str) -> str:
    return name.strip().capitalize()


people_without_project: list[str] = []

load_data = True
if load_data:
    df = pd.read_csv('./example_preferences - Sheet1.tsv', delimiter='\t')
    people_without_project.extend(['Hans', 'David'])
    # df = pd.read_csv('/home/jakub/Downloads/Coding Week 2025 - Code Review.tsv', delimiter='\t')
    df['I want to review this!'] = df['I want to review this!'].fillna('').astype(str)
    names = sorted([sanitize_name(name) for name in df['Name']])
    n = len(names)
    preferences = np.zeros((n, n), dtype=int)
    for name, preferred_mates in zip(df['Name'], df['I want to review this!']):
        if not preferred_mates:
            continue
        for mate in preferred_mates.split(','):
            preferences[names.index(sanitize_name(mate)), names.index(sanitize_name(name))] = 1
else:
    n = 16
    fake = Faker()
    names = set()
    while len(names) < n:
        names.add(fake.first_name())
    names = sorted(names)
    np.random.seed(42)
    preferences = (np.random.random((n, n)) < 0.15).astype(int)

edges = [[LpVariable(f"edge_{i}_{j}", cat="Binary") for i in range(n)] for j in range(n)]

prob = LpProblem("group_allocation", LpMaximize)
prob += lpSum([edges[i][j] * (
            preferences[i, j] + 100 - 1000 * (names[i] in people_without_project and names[j] in people_without_project))
               for i, j in product(range(n), repeat=2)])  # objective function

for i in range(n):
    prob += edges[i][i] == 0  # no self-edges
    prob += lpSum([edges[i][j] for j in range(n)]) <= 2  # Group of 3 max
    if names[i] in people_without_project:
        prob += lpSum([edges[i][j] for j in range(n)]) >= 2  # People without code must be in group of 3 
    else:
        prob += lpSum([edges[i][j] for j in range(n)]) >= 1  # Group of 2 at least

    for j, k in combinations([x for x in range(n) if x != i], 2):
        prob += edges[i][j] + edges[i][k] <= 1 + edges[j][k]  # transitivity

    for j in range(i):
        prob += edges[i][j] == edges[j][i]  # symmetry

# Change to PULP_CBC_CMD if you don't have GLPK installed
status = prob.solve(pulp.GLPK_CMD(msg=1, options=["--tmlim", "20"]))
# status = prob.solve(pulp.PULP_CBC_CMD(msg=1, timeLimit=20))


adjacency_matrix = np.array([[pulp.value(edges[i][j]) for i in range(n)] for j in range(n)])

# %%
teammates = {name: [names[j] for j, edge in enumerate(adjacency_matrix[i, :]) if edge]
             for i, name in enumerate(names)}
print(teammates)

graph = graphviz.Graph('Group_allocation', strict=False)

for i in range(n):
    for j in range(n):
        if adjacency_matrix[i, j] and i < j:
            graph.edge(names[i], names[j], color='green', penwidth='4')
        if preferences[i][j]:
            graph.edge(names[i], names[j], color='black', penwidth='1', dir='forward')

graph.view()
