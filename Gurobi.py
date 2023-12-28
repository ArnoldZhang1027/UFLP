import gurobipy as gp
from gurobipy import GRB

def gurobiSolver(opening_cost, service_cost, N):
    m = gp.Model()
    y = {}
    x = {}
    for i in range(0, N):
        y[i] = m.addVar(vtype=GRB.BINARY, name="y%d" % i)
        for j in range(0, N):
            x[i, j] = m.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name="x%d%d" % (i, j))
    m.update()
    m.setObjective(gp.quicksum(y[i] * opening_cost[i] for i in range(N)) +
                   gp.quicksum(x[i, j] * service_cost[i][j] for i in range(N) for j in range(N)), GRB.MINIMIZE)
    m.update()
    for i in range(0, N):
        for j in range(0, N):
            m.addConstr(x[i, j] <= y[i])
    for j in range(N):
        m.addConstr(gp.quicksum(x[i, j] for i in range(N)) == 1)
    m.update()
    m.setParam('method', 1)
    m.optimize()
    status = m.Status
    if (status == GRB.UNBOUNDED):
        print("It is an unbounded model")
        print(m.Unbdray)
    elif (status == GRB.INFEASIBLE):
        print("It is an infeasible model")
    print("======================================")
    print("选址结果如下：")
    for i in range(N):
        if (y[i].X == 1):
            print("在编号为%d的地方选址" % (i + 1))
    print("======================================")
    print("设备提供服务方案如下：")
    u = 0
    for i in range(N):
        for j in range(N):
            if x[i, j].X != 0:
                print("在编号为%d的地方的设备为编号为%d的目的地提供服务,服务占比为%.3f" % (i + 1, j + 1, x[i, j].X))
    print("======================================")
    print("最优目标值为：%d" % m.ObjVal)
    ObjVal = m.ObjVal
    return ObjVal




