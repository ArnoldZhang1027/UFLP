import coptpy as cp
from coptpy import Envr, COPT

def coptSolver(opening_cost, service_cost, N):
    env = Envr()
    m = env.createModel()

    y = {}
    x = {}

    for i in range(0, N):
        y[i] = m.addVar(vtype=COPT.BINARY, name="y%d" % i)
        for j in range(0, N):
            x[i, j] = m.addVar(lb=0, ub=1, vtype=COPT.CONTINUOUS, name="x%d%d" % (i, j))

    m.setObjective(cp.quicksum(y[i] * opening_cost[i] for i in range(N)) +
                   cp.quicksum(x[i, j] * service_cost[i][j] for i in range(N) for j in range(N)), COPT.MINIMIZE)

    for i in range(0, N):
        for j in range(0, N):
            m.addConstr(x[i, j] <= y[i])

    for j in range(N):
        m.addConstr(cp.quicksum(x[i, j] for i in range(N)) == 1)

    m.solve()

    status = m.Status
    if (status == COPT.UNBOUNDED):
        print("It is an unbounded model")
        print(m.Unbdray)
    elif (status == COPT.INFEASIBLE):
        print("It is an infeasible model")

    print("======================================")
    print("选址结果如下：")
    for i in range(N):
        if y[i].X == 1:
            print("在编号为%d的地方选址" % (i + 1))

    print("======================================")
    print("设备提供服务方案如下：")
    for i in range(N):
        for j in range(N):
            if x[i, j].X != 0:
                print("在编号为%d的地方的设备为编号为%d的目的地提供服务,服务占比为%.3f" % (i + 1, j + 1, x[i, j].X))

    print("======================================")
    print("最优目标值为：%d" % m.ObjVal)
    ObjVal = m.ObjVal
    return ObjVal




# # 创建COPT模型
# N = 100
# model = cp.odel()
#
# # 创建变量
# y = model.add_variable(N, vtype='binary', name="y")
# x = model.add_variable((N, N), vtype='continuous', lb=0, ub=1, name="x")
#
# # 设置目标函数
# model.set_objective(
#     cp.dot(opening_cost, y) + cp.sum(cp.multiply(service_cost, x)),
#     sense='minimize'
# )
#
# # 添加约束
# for i in range(N):
#     model.add_constraint(x[i] <= y[i])
#
# for j in range(N):
#     model.add_constraint(cp.sum(x[:, j]) == 1)
#
# # 求解模型
# solver = cp.solver("gurobi")
# result = model.solve(solver)
#
# # 打印结果
# if result.is_success():
#     print("======================================")
#     print("选址结果如下：")
#     for i in range(N):
#         if result.vars['y'][i] == 1:
#             print("在编号为%d的地方选址" % (i + 1))
#
#     print("======================================")
#     print("设备提供服务方案如下：")
#     for i in range(N):
#         for j in range(N):
#             if result.vars['x'][i, j] != 0:
#                 print("在编号为%d的地方的设备为编号为%d的目的地提供服务,服务占比为%.3f" % (i + 1, j + 1, result.vars['x'][i, j]))
#
#     print("======================================")
#     print("最优目标值为：%.3f" % result.objective)
#
# else:
#     print("求解失败")

