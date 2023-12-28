import gurobipy as gp
from gurobipy import *
from readtxt import readtxtfun as rt

def callback(model, where):
    if where == GRB.Callback.MIPSOL:
        y = model.cbGetSolution(model.getVars())
        for i in range(model._N):
            for j in range(model._N):
                model._ds._beta[i * model._N + j].obj = y[i]
        model._ds.update()
        model._ds.optimize()
        if model._ds.status == GRB.OPTIMAL:
            for j in range(model._N):
                model.cbLazy(model._ds._alpha[j].X + \
                             sum(model._ds._beta[i * model._N + j].X * model._y[i]\
                                 for i in range(model._N)) <= model._z[j])

    elif (where == GRB.Callback.MIPNODE) and \
            (model.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL):
        y = model.cbGetNodeRel(model.getVars())
        for i in range(model._N):
            for j in range(model._N):
                model._ds._beta[i * model._N + j].obj = y[i]
        model._ds.update()
        model._ds.optimize()
        if model._ds.status == GRB.OPTIMAL:
            for j in range(model._N):
                model.cbLazy(model._ds._alpha[j].X + \
                             gp.quicksum(model._ds._beta[i * model._N + j].X \
                                         * model._y[i] \
                                         for i in range(model._N)) <= model._z[j])

class bnc:
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

        # Construct the DS model
        self.ds = gp.Model()
        self.ds.update()

        self.alpha = self.ds.addVars(self.N, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, obj=0)
        self.beta = self.ds.addVars(self.N * self.N, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=0, obj=0)
        self.ds.update()

        self.ds.setObjective(gp.quicksum(self.alpha[i] for i in range(self.N)) +
                             gp.quicksum(self.beta[j] for j in range(self.N * self.N)),
                             GRB.MAXIMIZE)
        self.ds.update()

        for i in range(self.N):
            for j in range(self.N):
                self.dscons.append(self.ds.addConstr(self.alpha[j] + self.beta[i * self.N + j]
                                                     <= float(self.service_cost[i][j])))
        self.ds.update()

    def bnc_solver(self):
        # Parameters settings
        self.ds.Params.InfUnbdInfo = 1
        self.ds.Params.OutputFlag = 0
        self.rmp.Params.OutputFlag = 0
        self.rmp.Params.LazyConstraints = 1

        #Register callback
        self.rmp._N = self.N
        self.rmp._y = self.y
        self.rmp._z = self.z
        self.rmp._rmpcons = self.rmpcons
        self.ds._alpha = self.alpha
        self.ds._beta = self.beta
        self.ds._dscons = self.dscons

        # Connect the RMP and the DS
        self.rmp._ds = self.ds

        #Solve
        self.rmp.optimize(callback)

    def report(self):
        print("Objective: %.6f" % self.rmp.objval)
