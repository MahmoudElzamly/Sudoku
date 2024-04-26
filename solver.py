import copy
import time
from random_sudoku_generator import Sudoku


def initialize_variable_domains_and_constraints(variables_domains, variables_arc_constraints, sudoku):
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
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 3 <= j <= 5:
                        n = 3
                        while n <= 5:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 6 <= j <= 8:
                        n = 6
                        while n <= 8:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    m += 1
            elif 3 <= i <= 5:
                m = 3
                while m <= 5:
                    if 0 <= j <= 2:
                        n = 0
                        while n <= 2:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 3 <= j <= 5:
                        n = 3
                        while n <= 5:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 6 <= j <= 8:
                        n = 6
                        while n <= 8:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    m += 1
            if 6 <= i <= 8:
                m = 6
                while m <= 8:
                    if 0 <= j <= 2:
                        n = 0
                        while n <= 2:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 3 <= j <= 5:
                        n = 3
                        while n <= 5:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    elif 6 <= j <= 8:
                        n = 6
                        while n <= 8:
                            if not (m == i and n == j):
                                variable_constraints.append((m, n))
                            n += 1
                    m += 1
            variables_arc_constraints[(i, j)] = variable_constraints

def arc_consistency(variables_domains,variables_arc_constraints,matrix):
    check_oneElement_not_set=[]
    for i in range(0,9):
        for j in range(0, 9):
            if len(variables_domains[(i,j)])==1 and matrix[i][j]!=0:
                value=variables_domains[(i,j)][0]
                constr=variables_arc_constraints[(i,j)]
                for k in constr:
                    if value in variables_domains[k]:
                        # variables_domains.update({k:})
                        variables_domains[k].remove(value)



    return variables_domains

def backtracking(variables_domains, variables_arc_constraints, sudoku_mat, solution,Domains):
    modified = 0
    for i in range(0, 9):
        for j in range(0, 9):
            print(i, j, '....', (variables_domains[(i, j)]), sudoku_mat[i][j])
            if len(variables_domains[(i, j)]) == 0:
                return sudoku_mat, False,Domains
            if len(variables_domains[(i, j)]) == 1 and sudoku_mat[i][j] == 0:
                sudoku_mat[i][j] = variables_domains[(i, j)][0]
                solution.append(copy.deepcopy(sudoku_mat))
                arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
                Domains.append(variables_domains)
                modified = 1
                if is_complete(sudoku_mat):
                    return sudoku_mat, solution,Domains
                else:
                    return backtracking(variables_domains, variables_arc_constraints, sudoku_mat, solution,Domains)
    # arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)

    if modified == 0:
        MRV_Xind = 0
        MRV_Yind = 0
        minnum = 10
        for i in range(0, 9):
            for j in range(0, 9):
                if len(variables_domains[(i, j)]) < minnum and len(variables_domains[(i, j)]) >= 2:
                    minnum = len(variables_domains[(i, j)])
                    MRV_Xind = i
                    MRV_Yind = j
        vaules = copy.deepcopy(variables_domains[(MRV_Xind, MRV_Yind)])
        dm = copy.deepcopy(variables_domains)
        cst = copy.deepcopy(variables_arc_constraints)
        sol = copy.deepcopy(solution)
        Dom_stored=copy.deepcopy(Domains)
        print('Mrv_____________________', MRV_Xind, MRV_Yind)
        mat = copy.deepcopy(sudoku_mat)
        while len(vaules) != 0:
            k = vaules.pop()
            p = []
            p.append(k)
            variables_domains.update({(MRV_Xind, MRV_Yind): p})

            #print(variables_domains[(i, j)])
            # arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
            k, v,d = backtracking(variables_domains, variables_arc_constraints, sudoku_mat, sol,Domains)
            if v == False:
                variables_domains = copy.deepcopy(dm)
                variables_arc_constraints = copy.deepcopy(cst)
                sudoku_mat = copy.deepcopy(mat)
                sol = copy.deepcopy(solution)
                Domains= copy.deepcopy(Dom_stored)
                if len(vaules) == 0:

                    return sudoku_mat,False,Domains
            else:
                solution = v
                Domains=d
                if is_complete(k):
                    return k, solution,Domains

                    #print("tefgayhcdsjcsdmkc")
                    # backtracking(variables_domains, variables_arc_constraints, sudoku_mat)
        # variables_domains[(i, j)]=copy.deepcopy(vaules)
    # else:
    #     # arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
    #     if is_complete(sudoku_mat):
    #         return sudoku_mat, solution
    #     else:
    #         for i in range(0, 9):
    #             # pass
    #             print(sudoku_mat[i])
    #         # time.sleep(10)
    #         return backtracking(variables_domains, variables_arc_constraints, sudoku_mat, solution)

    # arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
    # if is_complete(sudoku_mat):
    #     return sudoku_mat, solution
    # for i in range(0, 9):
    #     print(sudoku_mat[i])
    # # print("possitioon")
    # return backtracking(variables_domains, variables_arc_constraints, sudoku_mat, solution)

def is_complete(sudoku_mat):
    for i in range(0, 9):
        for j in range(0, 9):
            if sudoku_mat[i][j] == 0:
                return False
    return True


def print_mat(mat):
    for i in range(0, 9):
        print(mat[i])
    print("_____________________")



def solve_sudoku(sudoku):
    variables_domains = {}
    variables_arc_constraints = {}
    initialize_variable_domains_and_constraints(variables_domains, variables_arc_constraints, sudoku)
    n = arc_consistency(variables_domains, variables_arc_constraints, sudoku.mat)
    # backtracking(variables_domains,variables_arc_constraints,sudoku.mat)
    _, v,d = backtracking(variables_domains, variables_arc_constraints, sudoku.mat, [copy.deepcopy(sudoku.mat)],[copy.deepcopy(n)])

    for i in range(0,len(d)):
        print(i,d[i])
    return v


