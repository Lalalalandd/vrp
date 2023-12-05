from pulp import *

# Data
j = 15
k1 = 1
k2 = 1
k3 = 1
cap1 = 360
cap2 = 800
cap3 = 1350
cost = 850
distance = [
    [55.3, 53.2, 49.2, 54, 56, 52, 55, 60.9, 61, 62.2, 60.8, 60.4, 59.9, 64.1, 53.3],
    [55.3, 9, 10.6, 5.9, 10, 4.5, 5.8, 12.1, 13.6, 9.9, 5.3, 8.5, 11.6, 8, 2.5],
    [53.2, 9, 7.4, 4.9, 4.2, 6.3, 5.9, 13.6, 13.7, 13.1, 11.6, 13.7, 10.1, 13.5, 7.7],
    [49.2, 10.6, 7.4, 9.1, 13.8, 7, 10.2, 14.8, 16.3, 17.4, 14.4, 15.5, 4.6, 16.5, 8],
    [54, 5.9, 4.9, 9.1, 6.4, 3, 2.3, 6.9, 8.4, 8.1, 7.4, 6.2, 9.7, 9.4, 5],
    [56, 10, 4.2, 13.8, 6.4, 8.8, 6.4, 7.2, 9.8, 13.2, 12.2, 11.3, 15.5, 13.5, 10.8],
    [52, 4.5, 6.3, 7, 3, 8.8, 4.9, 9.5, 11, 11.1, 8.6, 9.2, 8.4, 10.6, 2.5],
    [55, 5.8, 5.9, 10.2, 2.3, 6.4, 4.9, 6.1, 7.6, 7.8, 7.1, 5.9, 10.8, 9.1, 6.7],
    [60.9, 12.1, 13.6, 14.8, 6.9, 7.2, 9.5, 6.1, 1.5, 7.8, 13.4, 6.8, 16.9, 9.7, 12.2],
    [61, 13.6, 13.7, 16.3, 8.4, 9.8, 11, 7.6, 1.5, 8.4, 14.6, 7.5, 18.1, 10.3, 13.3],
    [62.2, 9.9, 13.1, 17.4, 8.1, 13.2, 11.1, 7.8, 7.8, 8.4, 7.6, 2.5, 17.5, 1.9, 10],
    [60.8, 5.3, 11.6, 14.4, 7.4, 12.2, 8.6, 7.1, 13.4, 14.6, 7.6, 7, 15.5, 4.7, 6.7],
    [60.4, 8.5, 13.7, 15.5, 6.2, 11.3, 9.2, 5.9, 6.8, 7.5, 2.5, 7, 16.6, 3.7, 9.1],
    [59.9, 11.6, 10.1, 4.6, 9.7, 15.5, 8.4, 10.8, 16.9, 18.1, 17.5, 15.5, 16.6, 15.4, 7.3],
    [64.1, 8, 13.5, 16.5, 9.4, 13.5, 10.6, 9.1, 9.7, 10.3, 1.9, 4.7, 3.7, 15.4, 9.6],
    [53.3, 2.5, 7.7, 8, 5, 10.8, 2.5, 6.7, 12.2, 13.3, 10, 6.7, 9.1, 7.3, 9.6]
]
demand_CDD = [350, 360, 350, 0, 360, 350, 360, 350, 0, 0, 0, 0, 0, 0, 0]
demand_fuso = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 800, 800, 800, 0]
demand_fusotronton = [0, 0, 0, 1350, 0, 0, 0, 0, 1050, 1350, 1350, 0, 0, 0, 1050]

# Create variables
x = LpVariable.dicts('route', [(a, b, c) for a in range(j) for b in range(j) for c in range(3)], 0, 1, LpBinary)
u = LpVariable.dicts('u', range(j), 0, j - 1, LpInteger)
# Create the problem
prob = LpProblem("VehicleRoutingProblem", LpMinimize)

# Objective function
prob += lpSum(x[a, b, c] * distance[a][b] * cost for a in range(j) for b in range(j) for c in range(3))

# Constraints
# 1. Each destination is visited at least once by each truck
for dest in range(1, j):
    prob += lpSum(x[a, dest, k] for a in range(j) for k in range(3)) == 1

# 2. Demand constraint for each route
for jj in range(1, j):
    for i in range(j) :
        for k in range(3) :
            if k == 0 :
                prob += lpSum(x[i, jj, k] * demand_CDD[jj]) <= cap1
            elif k == 1 :
                prob += lpSum(x[i, jj, k] * demand_fuso[jj]) <= cap2
            else :
                prob += lpSum(x[i, jj, k] * demand_fusotronton[jj]) <= cap3


# 3. Capacity constraint for each truck
for k in range(3):
    prob += lpSum(x[i, jj, k] * [demand_CDD, demand_fuso, demand_fusotronton][k][jj] for i in range(j) for jj in range(1, j)) <= [cap1, cap2, cap3][k]

# 4. Leaving each destination
for jj in range(1, j):
    prob += lpSum(x[i, jj, k] for i in range(j) for k in range(3)) == lpSum(x[jj, i, k] for i in range(j) for k in range(3))

# 5. Returning to the source
for k in range(3):
    prob += lpSum(x[i, 0, k] for i in range(1, j)) == 1

# 6. No sub-routes
for jj in range(1, j):
    prob += lpSum(x[jj, i, k] for i in range(j) for k in range(3)) == 1


# # Solve the problem
prob.solve()

# # Display the solution
for v in prob.variables():
    if v.varValue > 0:
        print(f"{v.name}: {v.varValue}")

print(f"Total Cost: {value(prob.objective)}")