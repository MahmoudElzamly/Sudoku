from time import sleep

from gui import GUI
import queue
from random_sudoku_generator import Sudoku
from validator import isValidSudoku
import copy
N = 9
K = 40
sudoku = Sudoku(N, K)
sudoku.fillValues()
#

variables_domains = {}
variables_arc_constraints = {}
variables_that_require_consistency_enforcement = queue.Queue()
for i in range(0,9):
    print(sudoku.mat[i])

def initialize_variable_domains_and_constraints():
    for i in range(9):
        for j in range(9):
            if sudoku.mat[i][j] == 0:
                variables_domains[(i, j)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            else:
                variables_domains[(i, j)] = [sudoku.mat[i][j]]

            variable_constraints = []
            # Setting row constraints
            for k in range(9):
                if k != j:
                    variable_constraints.append((i, k))

            # Setting column constraints
            for k in range(9):
                if k != i:
                    variable_constraints.append((k, j))

            # Setting sub grid constraints
            if 0 <= i <= 2:
                m = 0
                while m <= 2:
                    if 0 <= j <= 2:
                        n = 0
                        while n <= 2:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 3 <= j <= 5:
                        n = 3
                        while n <= 5:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 6 <= j <= 8:
                        n = 6
                        while n <= 8:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    m += 1
            elif 3 <= i <= 5:
                m = 3
                while m <= 5:
                    if 0 <= j <= 2:
                        n = 0
                        while n <= 2:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 3 <= j <= 5:
                        n = 3
                        while n <= 5:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 6 <= j <= 8:
                        n = 6
                        while n <= 8:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    m += 1
            if 6 <= i <= 8:
                m = 6
                while m <= 8:
                    if 0 <= j <= 2:
                        n = 0
                        while n <= 2:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 3 <= j <= 5:
                        n = 3
                        while n <= 5:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 6 <= j <= 8:
                        n = 6
                        while n <= 8:
                            if not(m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    m += 1
            variables_arc_constraints[(i, j)] = variable_constraints


initialize_variable_domains_and_constraints()
for key in variables_domains:
    print(f"{key}: {variables_domains[key]}")
print("///////////////////////")
for key in variables_arc_constraints:
    print(f"{key}: {variables_arc_constraints[key]}")
# variables_domains[(1, 5)].remove(5)
# print((variables_domains[(1, 5)].remove(7)))
print((variables_domains[(1, 5)]))

def arc_consistency(variables_domains,variables_arc_constraints,matrix):
    check_oneElement_not_set=[]
    for i in range(0,9):
        for j in range(0, 9):
            if len(variables_domains[(i,j)])==1:
                value=variables_domains[(i,j)][0]
                constr=variables_arc_constraints[(i,j)]
                for k in constr:
                    if value in variables_domains[k]:
                        variables_domains[k].remove(value)
                        if len(variables_domains[k])==1:
                            check_oneElement_not_set.append((i,j))
    # print(check_oneElement_not_set)

    # while len(check_oneElement_not_set)!=0:
    #     i,j=check_oneElement_not_set.pop()
    #     constr = variables_arc_constraints[(i, j)]
    #     for k in constr:
    #         if value in variables_domains[k]:
    #             variables_domains[k].remove(value)
    #             if len(variables_domains[k]) == 1:
    #                 check_oneElement_not_set.append((i, j))
    # print(check_oneElement_not_set)

    return variables_domains
def is_compelete(sudoku_mat):
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku_mat[i][j]==0:
                return False
    return True
def print_mat(mat):
    for i in range(0, 9):
        print(mat[i])
    print("___________________________________________________________")
def backtracking(variables_domains,variables_arc_constraints,sudoku_mat,solution):

    modified=0
    for i in range(0,9):
        for j in range(0, 9):
            print(i,j,'....',(variables_domains[(i,j)]),sudoku_mat[i][j])
            if len(variables_domains[(i, j)]) == 0:
                return False
            if len(variables_domains[(i,j)])==1 and sudoku_mat[i][j]==0:
                sudoku_mat[i][j]=variables_domains[(i,j)][0]
                solution.append(copy.deepcopy(sudoku_mat))

                modified+=1
    arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)

    if modified==0:
        MRV_Xind=0
        MRV_Yind=0
        minnum=10
        for i in range(0, 9):
            for j in range(0, 9):
                if len(variables_domains[(i, j)]) <minnum and len(variables_domains[(i, j)])>=2:
                    minnum=len(variables_domains[(i, j)])
                    MRV_Xind = i
                    MRV_Yind = j
        vaules = copy.deepcopy(variables_domains[(MRV_Xind, MRV_Yind)])
        dm=copy.deepcopy(variables_domains)
        cst=copy.deepcopy(variables_arc_constraints)
        sol=copy.deepcopy(solution)
        print('Mrv',MRV_Xind,MRV_Yind)
        mat=copy.deepcopy(sudoku_mat)
        while len(vaules)!=0:
            k=vaules.pop()
            # print(k)
            p=[]
            p.append(k)
            variables_domains.update({(MRV_Xind,MRV_Yind):p})

            print(variables_domains[(i, j)])
            # arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
            if backtracking(variables_domains, variables_arc_constraints, sudoku_mat,sol)==False:
                variables_domains=dm
                variables_arc_constraints=cst
                sudoku_mat=mat
                k = vaules.pop(0)
                variables_domains[(i, j)] = []
                variables_domains[(i, j)].append(k)
                sol = copy.deepcopy(solution)


            else:

                if is_compelete(sudoku_mat):
                    return sudoku_mat,solution
                else:
                    print("tefgayhcdsjcsdmkc")
                    # backtracking(variables_domains, variables_arc_constraints, sudoku_mat)
        # variables_domains[(i, j)]=copy.deepcopy(vaules)
    else:
        arc_consistency(variables_domains, variables_arc_constraints,sudoku_mat)
        if is_compelete(sudoku_mat):
            return sudoku_mat,solution
        else:
            for i in range(0,9):
                print(sudoku_mat[i])
            # sleep(1)
            return backtracking(variables_domains, variables_arc_constraints, sudoku_mat,solution)






    arc_consistency(variables_domains,variables_arc_constraints,sudoku_mat)
    for i in range(0, 9):
        print(sudoku_mat[i])
#
# sudoku.mat=[[1, 9, 6, 2, 4, 0, 5, 0, 7],
# [7, 5, 4, 0, 0, 0, 0, 6, 3],
# [2, 3, 8, 6, 5, 7, 0, 1, 0],
# [0, 0, 0, 9, 0, 0, 7, 5, 0],
# [4, 0, 7, 5, 0, 0, 3, 9, 0],
# [0, 0, 5, 7, 3, 1, 8, 0, 0],
# [5, 4, 0, 0, 0, 0, 6, 0, 0],
# [0, 0, 0, 0, 0, 0, 1, 0, 0],
# [6, 0, 0, 0, 1, 5, 0, 7, 9]]

n=arc_consistency(variables_domains,variables_arc_constraints,sudoku.mat)
# backtracking(variables_domains,variables_arc_constraints,sudoku.mat)
k,v=backtracking(variables_domains,variables_arc_constraints,sudoku.mat,[copy.deepcopy(sudoku.mat)])
for mat in v:
    print_mat(mat)
print(n)
print(type(variables_domains[(3,3)]))

print(type(sudoku.mat))
gui = GUI(sudoku.mat)