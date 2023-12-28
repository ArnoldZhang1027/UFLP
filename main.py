import matplotlib
from Gurobi import gurobiSolver
# from gurobipy import GRB
# import gurobipy as gp
from COPT import coptSolver
# from Benders_Gurobi import benders, mycallback
from readtxt import readtxtfun
import time
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import numpy as np
from benders_gurobi_onecut import origin_bendersSolver, origin_bendersSolver
from benders_greedy_onecut import greedy_bendersSolver, greedy_assignment
from benders_greedy_multicuts import multicuts_bendersSolver
from bnc_gurobi_onehundredcuts import callback, bnc
from bnc_greedy_onehundredcuts import bnc_greedy
import threading
import sys

def set_timeout_flag():
    global timeout_flag
    timeout_flag = True
    return timeout_flag

if __name__ == '__main__':
    N = 100
    pro_no = 30

    print("*******************************")
    print("现在程序在利用Gurobi求解")
    print("*******************************")
    t_1 = []
    start_time = time.time()
    t_1.append(start_time)
    for i in range(pro_no):
        txtname = str(i + 1) + '23UnifS.txt'
        print("正在求解%s数据集" % txtname)
        opening_cost, service_cost = readtxtfun(txtname)
        opening_cost = opening_cost[0:N]
        service_cost = np.array(service_cost)[0:N, 0:N]
        print(opening_cost)
        print(service_cost)
        gurobiSolver(opening_cost, service_cost, N)
        t_1.append(time.time())
    delta_t = t_1[0]
    per_t_1 = np.zeros(len(t_1))
    for i in range(len(t_1)):
        t_1[i] -= delta_t
        if i == 0:
            per_t_1[i] = t_1[i]
        else:
            per_t_1[i] = t_1[i] - t_1[i-1]

    print("*******************************")
    print("现在程序在利用COPT求解")
    print("*******************************")
    t_2 = []
    start_time = time.time()
    t_2.append(start_time)
    for i in range(pro_no):
        txtname = str(i + 1) + '23UnifS.txt'
        print("正在求解%s数据集" % txtname)
        opening_cost, service_cost = readtxtfun(txtname)
        opening_cost = opening_cost[0:N]
        service_cost = np.array(service_cost)[0:N, 0:N]
        coptSolver(opening_cost, service_cost, N)
        t_2.append(time.time())
    delta_t = t_2[0]
    per_t_2 = np.zeros(len(t_2))
    for i in range(len(t_2)):
        t_2[i] -= delta_t
        if i == 0:
            per_t_2[i] = t_2[i]
        else:
            per_t_2[i] = t_2[i] - t_2[i - 1]


    # print("*******************************")
    # print("现在程序在利用benders_gurobi_onecut求解")
    # print("*******************************")
    # t_3 = []
    # start_time = time.time()
    # t_3.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     opening_cost, service_cost = readtxtfun(txtname)
    #     opening_cost = opening_cost[0:N]
    #     service_cost = np.array(service_cost)[0:N,0:N]
    #     origin_bendersSolver(opening_cost, service_cost, N)
    #     solve_end_time = time.time()
    #     t_3.append(time.time())
    # delta_t = t_3[0]
    # for i in range(len(t_3)):
    #     t_3[i] -= delta_t

    # print("*******************************")
    # print("现在程序在利用benders_gurobi_onecut求解")
    # print("*******************************")
    # t_4 = []
    # start_time = time.time()
    # t_4.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     opening_cost, service_cost = readtxtfun(txtname)
    #     opening_cost = opening_cost[0:N]
    #     service_cost = np.array(service_cost)[0:N, 0:N]
    #     greedy_bendersSolver(opening_cost, service_cost, N)
    #     solve_end_time = time.time()
    #     t_4.append(time.time())
    # delta_t = t_4[0]
    # for i in range(len(t_4)):
    #     t_4[i] -= delta_t

    # print("*******************************")
    # print("现在程序在利用benders_greedy_onecut求解")
    # print("*******************************")
    # t_4 = []
    # start_time = time.time()
    # t_4.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     opening_cost, service_cost = readtxtfun(txtname)
    #     opening_cost = opening_cost[0:N]
    #     service_cost = np.array(service_cost)[0:N, 0:N]
    #     greedy_bendersSolver(opening_cost, service_cost, N)
    #     t_4.append(time.time())
    # delta_t = t_4[0]
    # for i in range(len(t_4)):
    #     t_4[i] -= delta_t

    # print("*******************************")
    # print("现在程序在利用benders_greedy_100cuts求解")
    # print("*******************************")
    # V = 1
    # t_5 = []
    # start_time = time.time()
    # t_5.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     opening_cost, service_cost = readtxtfun(txtname)
    #     opening_cost = opening_cost[0:N]
    #     service_cost = np.array(service_cost)[0:N, 0:N]
    #     multicuts_bendersSolver(opening_cost, service_cost, N, V)
    #     t_5.append(time.time())
    # delta_t = t_5[0]
    # for i in range(len(t_5)):
    #     t_5[i] -= delta_t
    # #
    # print("*******************************")
    # print("现在程序在利用benders_greedy_50cuts求解")
    # print("*******************************")
    # V = 2
    # t_6 = []
    # start_time = time.time()
    # t_6.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     opening_cost, service_cost = readtxtfun(txtname)
    #     opening_cost = opening_cost[0:N]
    #     service_cost = np.array(service_cost)[0:N, 0:N]
    #     multicuts_bendersSolver(opening_cost, service_cost, N, V)
    #     t_6.append(time.time())
    # delta_t = t_6[0]
    # for i in range(len(t_6)):
    #     t_6[i] -= delta_t

    # print("*******************************")
    # print("现在程序在利用bnc_gurobi_100cuts求解")
    # print("*******************************")
    # t_7 = []
    # start_time = time.time()
    # t_7.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     solver = bnc()
    #     solver.readfile(txtname)
    #     solver.build_model()
    #     solver.bnc_solver()
    #     solver.report()
    #     t_7.append(time.time())
    # delta_t = t_7[0]
    # per_t_7 = np.zeros(len(t_7))
    # for i in range(len(t_7)):
    #     t_7[i] -= delta_t
    #     if i == 0:
    #         per_t_7[i] = t_7[i]
    #     else:
    #         per_t_7[i] = t_7[i] - t_7[i - 1]
    #
    # print("*******************************")
    # print("现在程序在利用bnc_greedy_100cuts求解")
    # print("*******************************")
    # t_8 = []
    # start_time = time.time()
    # t_8.append(start_time)
    # for i in range(pro_no):
    #     txtname = str(i + 1) + '23UnifS.txt'
    #     print("正在求解%s数据集" % txtname)
    #     solver = bnc_greedy()
    #     solver.readfile(txtname)
    #     solver.build_model()
    #     solver.bnc_solver()
    #     solver.report()
    #     t_8.append(time.time())
    # delta_t = t_8[0]
    # per_t_8 = np.zeros(len(t_8))
    # for i in range(len(t_8)):
    #     t_8[i] -= delta_t
    #     if i == 0:
    #         per_t_8[i] = t_8[i]
    #     else:
    #         per_t_8[i] = t_8[i] - t_8[i - 1]
    #
    #画图
    # x = np.linspace(1, pro_no, pro_no)
    x = np.linspace(0, pro_no, pro_no+1)
    # plt.ylim(bottom=0)
    plt.plot(x, per_t_1, label='Gurobi', linestyle='-', color='green')
    plt.plot(x, per_t_2, label='COPT', linestyle='-', color='black')
    # plt.plot(x, t_3, label='Benders_Gurobi_1cut', linestyle='-', color='orange')
    # plt.plot(x, t_4, label='Benders_Greedy_1cut', linestyle='-', color='blue')
    # plt.plot(x, t_5, label='Benders_Greedy_100cuts', linestyle='-', color='red')
    # plt.plot(x, t_6, label='Benders_Greedy_50cuts', linestyle='-', color='purple')
    # plt.plot(x, t_7, label='BnC_Gurobi_100cuts', linestyle='-', color='brown')
    # plt.plot(x, t_8, label='BnC_Greedy_100cuts', linestyle='-', color='pink')

    # plt.plot(x, per_t_1[1:], label='Gurobi', linestyle='-', color='green')
    # plt.plot(x, per_t_2[1:], label='COPT', linestyle='-', color='black')
    # plt.plot(x, per_t_7[1:], label='BnC_Gurobi_100cuts', linestyle='-', color='brown')
    # plt.plot(x, per_t_8[1:], label='BnC_Greedy_100cuts', linestyle='-', color='pink')
    plt.legend()
    plt.title('Run time for each problem')
    plt.xlabel('Problem No.(1-30)')
    plt.ylabel('Time per problem')
    plt.show()




