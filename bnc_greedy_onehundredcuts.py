import gurobipy as gp
from gurobipy import *
from readtxt import readtxtfun as rt
import numpy as np
from benders_greedy_onecut import greedy_assignment

def callback(model, where):
    if where == GRB.Callback.MIPSOL:
        lb_new = model.cbGet(GRB.callback.MIPSOL_OBJBND)  # lb
        if lb_new >= model._lb[-1]:
            model._lb.append(lb_new)

            y = model.cbGetSolution(model.getVars())

            assignable_y = []
            for i in range(model._N):
                assignable_y.append(y[i])

            alpha = np.zeros(model._N)
            beta = np.zeros((model._N, model._N))
            x = np.zeros((model._N, model._N))
            service_cost = np.array(model._service_cost)
            for j in range(model._N):
                alpha_vector, beta_vector, x_vector = greedy_assignment(service_cost[:, j], assignable_y, model._N)
                alpha[j] = alpha_vector
                beta[:, j] = beta_vector
                x[:, j] = x_vector

            for j in range(model._N):
                model.cbLazy(alpha[j] + sum(beta[i, j] * model._y[i]
                                            for i in range(model._N)) <= model._z[j])


    elif (where == GRB.Callback.MIPNODE) and (model.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL):
        ub_new = model.cbGet(GRB.callback.MIPNODE_OBJBST)
        if ub_new < model._ub[-1]:
            model._ub.append(ub_new)

            y = model.cbGetNodeRel(model.getVars())

            assignable_y = []
            for i in range(model._N):
                assignable_y.append(y[i])

            alpha = np.zeros(model._N)
            beta = np.zeros((model._N, model._N))
            x = np.zeros((model._N, model._N))
            service_cost = np.array(model._service_cost)
            for j in range(model._N):
                alpha_vector, beta_vector, x_vector = greedy_assignment(service_cost[:, j], assignable_y, model._N)
                alpha[j] = alpha_vector
                beta[:, j] = beta_vector
                x[:, j] = x_vector

            for j in range(model._N):
                model.cbLazy(alpha[j] + sum(beta[i, j] * model._y[i] for i in range(model._N)) <= model._z[j])

class bnc_greedy:
    def __init__(self):
        self.N = 100

        self.rmpcons = []
        self.dscons = []

    def readfile(self, filename):
        self.opening_cost, self.service_cost = rt(filename)
        for i in range(self.N):
            self.opening_cost[i] = float(self.opening_cost[i])
            for j in range(self.N):
                self.service_cost[i][j] = float(self.service_cost[i][j])
        self.lb = [float('-inf')]
        self.ub = [float('inf')]
    def build_model(self):
        # Construct the RMP model
        self.rmp = gp.Model()
        self.rmp.update()

        self.y = self.rmp.addVars(self.N, vtype=GRB.BINARY, obj=0)
        self.z = self.rmp.addVars(self.N, vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, obj=0)
        self.rmp.update()

        self.rmp.setObjective(gp.quicksum(self.opening_cost[i] * self.y[i] for i in range(self.N))
                              + gp.quicksum(self.z[i] for i in range(self.N)), GRB.MINIMIZE)
        self.rmp.update()

        self.rmpcons.append(self.rmp.addConstr(gp.quicksum(self.y[i] for i in range(self.N)) >= 1))
        self.rmp.update()

    def bnc_solver(self):
        # Parameters settings
        self.rmp.Params.OutputFlag = 0
        self.rmp.Params.LazyConstraints = 1

        #Register callback
        self.rmp._N = self.N
        self.rmp._y = self.y
        self.rmp._z = self.z
        self.rmp._service_cost = self.service_cost
        self.rmp._lb = self.lb
        self.rmp._ub = self.ub

        #Solve
        self.rmp.optimize(callback)

    def report(self):
        print("Objective: %.6f" % self.rmp.objval)
