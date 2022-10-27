# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 10:22:03 2022

@author: grace_elizabeth
"""

from gurobipy import *

try:
    
    #Create lists
    a = [8, 8, 10, 16, 35]
    b = [20, 10, 20, 30, 20]
    
    cost_c = 1
    cost_d = 1
    flow_f = 1
    flow_g = [
        [7, 7, 5, 4, 2],
        [3, 2, 4, 5, 2]
        ]
    
    #indices
    new = 2 #new facilities to be placed
    old = len(a) #existing facilities in network
    
    #Create model
    m = Model("Example 4.1")
    
    x = m.addVars(new, vtype = GRB.CONTINUOUS, name = "x-coordinate")
    y = m.addVars(new, vtype = GRB.CONTINUOUS, name = "y-coordinate")
    xp = m.addVars(new, new, lb = 0, vtype = GRB.CONTINUOUS, name = "x-positive")
    xn = m.addVars(new, new, lb = 0, vtype = GRB.CONTINUOUS, name = "x-negative")
    yp = m.addVars(new, new, lb = 0, vtype = GRB.CONTINUOUS, name = "y-positive")
    yn = m.addVars(new, new, lb = 0, vtype = GRB.CONTINUOUS, name = "y-negative")
    xap = m.addVars(new, old, lb = 0, vtype = GRB.CONTINUOUS, name = "x-a-positive")
    xan = m.addVars(new, old, lb = 0, vtype = GRB.CONTINUOUS, name = "x-a-negative")
    ybp = m.addVars(new, old, lb = 0, vtype = GRB.CONTINUOUS, name = "y-b-positive")
    ybn = m.addVars(new, old, lb = 0, vtype = GRB.CONTINUOUS, name = "y-b-negative")
    
    #Set objective fuction
    m.setObjective(quicksum(cost_c * flow_f * (xp[i,j] + xn[i,j] + yp[i,j] + yn[i,j]) for i in range(new) for j in range(new)) + quicksum(cost_d * flow_g[i][j] * (xap[i,j] + xan[i,j] + ybp[i,j] + ybn[i,j]) for i in range(new) for j in range(old)), GRB.MINIMIZE)
    
    #Write constraints
    for i in range(new):
        for j in range (new):
            m.addConstr(x[i] - x[j] == xp[i,j] - xn[i,j], name = "4.5")
            m.addConstr(y[i] - y[j] == yp[i,j] - yn[i,j], name = "4.7")
            
    for i in range(new):
        for j in range (old):       
            m.addConstr(x[i] - a[j] == xap[i,j] - xan[i,j], name = "4.9")
            m.addConstr(y[i] - b[j] == ybp[i,j] - ybn[i,j], name = "4.11")

    #Call Gurobi Optimizer
    m.optimize()
    if m.status == GRB.OPTIMAL:
       for v in m.getVars():
           if v.x > 0:
               print('%s = %g' % (v.varName, v.x)) 
       print('Obj = %f' % m.objVal)
    elif m.status == GRB.INFEASIBLE:
       
       print('LP is infeasible.')
    elif m.status == GRB.UNBOUNDED:
       print('LP is unbounded.')
except GurobiError:
    print('Error reported')