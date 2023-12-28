import os

def readtxtfun(txtname):
    current_directory = os.getcwd()
    folder_name = "data"
    folder_path = os.path.join(current_directory, folder_name)

    file_name = txtname
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines = lines[2:]

    opening_cost = []
    for line in lines:
        line = line.split()
        opening_cost.append(line[1])

    rows, cols = 100, 100
    service_cost = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(100):
        line = lines[i]
        line = line.split()
        for j in range(100):
            service_cost[i][j] = line[j + 2]

    return opening_cost, service_cost