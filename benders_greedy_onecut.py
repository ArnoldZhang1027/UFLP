import gurobipy as gp
from gurobipy import GRB
import numpy as np


def greedy_assignment(service_cost_vector, y, N):
    y = np.array(y)
    not_zero_pos = []
    for i in range(N):
        if y[i] != 0:
            not_zero_pos.append(i)

    service_cost_vector = np.array(service_cost_vector)
    available_facility = service_cost_vector[not_zero_pos]
    index = np.argmin(available_facility.astype(int))
    k = not_zero_pos[index]

    x = np.zeros(N)
    alpha = np.zeros(1)
    beta = np.zeros(N)
    for i in range(N):
        if i == k:
            x[i] = 1
        else:
            x[i] = 0

    for i in range(N):
        alpha = float(service_cost_vector[k])
        if float(service_cost_vector[i]) <= float(service_cost_vector[k]):
            beta[i] = float(service_cost_vector[i]) - float(service_cost_vector[k])
        else:
            beta[i] = 0

    return alpha, beta, x

    # assignable_y = []
    # for i in range(N):
    #     if y[i] != 0:
    #         assignable_y.append(i)
    #
    # service_cost = np.array(service_cost)
    # for i in range(N):
    #     index = np.argmin(service_cost[assignable_y, i])
    #     assignment[i] = assignable_y[index]
    #
    # return assignment


def greedy_bendersSolver(opening_cost, service_cost, N):
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
    rmp.Params.OutputFlag = 0


    while flag == 0:
        print('------------这是第 %d 次迭代------------' % k)
        rmp.Params.method = 1
        rmp.Params.nodemethod = 1
        rmp.optimize()

        assignable_y = []
        for i in range(N):
            assignable_y.append(y[i].X)

        alpha = np.zeros(N)
        beta = np.zeros((N, N))
        x = np.zeros((N, N))
        service_cost = np.array(service_cost)
        for j in range(N):
            alpha_vector, beta_vector, x_vector = greedy_assignment(service_cost[:, j], assignable_y, N)
            alpha[j] = alpha_vector
            beta[:, j] = beta_vector
            x[:, j] = x_vector

        Obj = 0
        for i in range(N):
            Obj += alpha[i]
            for j in range(N):
                Obj += beta[i, j] * y[i].X

        if Obj > z.X:
            print('ds.ObjVal=%d' % Obj)
            print('z.x=%d' % z.X)
            print('此次迭代，ds.ObjVal>z.x, 对偶子问题可行，但是未得到最优解，因此要加入 optimality cut')
            rmp.addConstr(gp.quicksum(alpha[i] for i in range(N)) +
                          gp.quicksum(beta[i, j] * y[i] for j in range(N) for i in range(N)) <= z)
            rmp.update()

        else:
            print('ds.ObjVal=%d' % Obj)
            print('z.x=%d' % z.X)
            flag = 1
            print("ds.ObjVal=z.x, 找到了最优解！")

        k = k + 1

    print("======================================")
    print("选址结果如下：")
    for i in range(N):
        if y[i].X != 0:
            print("在编号为%d的地方选址" % (i + 1))

    print("======================================")
    print("设备提供服务方案如下：")
    for i in range(N):
        for j in range(N):
            if x[i, j] != 0:
                print("在编号为%d的地方的设备为编号为%d的目的地提供服务,服务占比为1.000" % (i+1, j+1))

    sum = gp.quicksum(float(opening_cost[i]) * y[i].X for i in range(N)) + z.X
    print("======================================")
    print('最优目标值为:', end='')
    print(sum)

