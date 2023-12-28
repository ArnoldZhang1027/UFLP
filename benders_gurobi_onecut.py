import gurobipy as gp
from gurobipy import *

def origin_bendersSolver(opening_cost, service_cost, N):
    ds = gp.Model()
    ds.update()

    alpha = ds.addVars(N, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY, obj=0, name='alpha')
    beta = ds.addVars(N*N, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=0, obj=0, name='beta')
    ds.update()

    for i in range(N):
        for j in range(N):
            x_i_j = ds.addConstr(alpha[j] + beta[i*N+j] <= float(service_cost[i][j]))
    ds.update()

    rmp = gp.Model()
    rmp.update()

    y = rmp.addVars(N, vtype=GRB.BINARY, obj=0, name='y')
    z = rmp.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, obj=0, name='z')
    rmp.update()

    rmp.setObjective(gp.quicksum(y[i] * opening_cost[i] for i in range(N)) + z, GRB.MINIMIZE)
    rmp.update()

    rmp.addConstr(gp.quicksum(y[i] for i in range(N)) >= 1)
    rmp.update()

    k = 1
    flag = 0
    ds.Params.InfUnbdInfo = 1
    ds.Params.OutputFlag = 0
    rmp.Params.OutputFlag = 0


    while flag == 0:
        print('------------这是第 %d 次迭代------------' % k)
        # Optimize
        rmp.Params.method = 1
        rmp.Params.nodemethod = 1
        rmp.optimize()

        ds.reset()
        ds.setObjective(gp.quicksum(alpha[i] for i in range(N)) +
                        gp.quicksum(y[i].X * gp.quicksum(beta[j] for j in range(i * N, (i + 1) * N)) for i in range(N)),
                        GRB.MAXIMIZE)

        ds.Params.method = 1

        ds.optimize()

        # if ds.status == GRB.UNBOUNDED:
        #     print('此次迭代，对偶子问题无界，因此要加入 feasibility cut，对应的极方向为')
        #     ray = ds.UnbdRay
        #     rmp.addConstr(gp.quicksum(ray[i] for i in range(N)) +
        #                   gp.quicksum(ray[i + N] * y[i // N] for i in range(N * N)) <= 0)
        #     rmp.optimize()

        if ds.ObjVal > z.x:
            print('ds.ObjVal=%d' % ds.ObjVal)
            print('z.x=%d' % z.x)
            print('此次迭代，ds.ObjVal>z.x, 对偶子问题可行，但是未得到最优解，因此要加入 optimality cut')
            rmp.addConstr(gp.quicksum(alpha[i].X for i in range(N)) +
                          gp.quicksum(beta[i].X * y[i // N] for i in range(N * N)) <= z)
            rmp.optimize()

        else:
            flag = 1
            print("ds.ObjVal=z.x, 找到了最优解！")

        k = k + 1

    sum = gp.quicksum(float(opening_cost[i])*y[i].X for i in range(N)) + z.X
    print('最优目标值为:', end='')
    print(sum)

