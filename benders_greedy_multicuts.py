import gurobipy as gp
from gurobipy import GRB
import numpy as np
from benders_greedy_onecut import greedy_assignment

def multicuts_bendersSolver(opening_cost, service_cost, N, V):
    rmp = gp.Model()
    rmp.update()

    y = rmp.addVars(N, vtype=GRB.BINARY, obj=0, name='y')
    z = rmp.addVars(N//V, vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY, obj=0, name='z')
    rmp.update()

    rmp.setObjective(gp.quicksum(y[i] * opening_cost[i] for i in range(N))
                     + gp.quicksum(z[i] for i in range(N//V)), GRB.MINIMIZE)
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

        sum_z = 0
        for i in range(N//V):
            sum_z += z[i].X

        Obj = 0
        for i in range(N):
            Obj += alpha[i]
            for j in range(N):
                Obj += beta[i, j] * y[i].X

        if Obj > sum_z:
            print('ds.ObjVal=%d' % Obj)
            print('z.x=%d' % sum_z)
            print('此次迭代，ds.ObjVal>z.x, 对偶子问题可行，但是未得到最优解，因此要加入 optimality cut')

            v = 1
            while v <= N//V:
                rmp.addConstr(gp.quicksum(alpha[i] for i in range((v-1)*V, v*V)) +
                              gp.quicksum(beta[i, j] * y[i] for j in range((v-1)*V, v*V) for i in range(N)) <= z[v-1])
                v += 1
            rmp.update()
            rmp.optimize()

        else:
            print('ds.ObjVal=%d' % Obj)
            print('z.x=%d' % sum_z)
            flag = 1
            print("ds.ObjVal=z.x, 找到了最优解！")

        k += 1

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
                print("在编号为%d的地方的设备为编号为%d的目的地提供服务,服务占比为1.000" % (i + 1, j + 1))

    sum = gp.quicksum(float(opening_cost[i]) * y[i].X for i in range(N)) + sum_z
    print("======================================")
    print('最优目标值为:', end='')
    print(sum)
