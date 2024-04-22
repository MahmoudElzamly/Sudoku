import copy

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


def arc_consistency(variables_domains, variables_arc_constraints, matrix):
    check_oneElement_not_set = []
    for i in range(0, 9):
        for j in range(0, 9):
            if len(variables_domains[(i, j)]) == 1:
                value = variables_domains[(i, j)][0]
                constr = variables_arc_constraints[(i, j)]
                for k in constr:
                    if value in variables_domains[k]:
                        variables_domains[k].remove(value)
                        if len(variables_domains[k]) == 1:
                            check_oneElement_not_set.append((i, j))
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


def backtracking(variables_domains, variables_arc_constraints, sudoku_mat, solution):
    modified = 0
    for i in range(0, 9):
        for j in range(0, 9):
            print(i, j, '....', (variables_domains[(i, j)]), sudoku_mat[i][j])
            if len(variables_domains[(i, j)]) == 0:
                return sudoku_mat, False
            if len(variables_domains[(i, j)]) == 1 and sudoku_mat[i][j] == 0:
                sudoku_mat[i][j] = variables_domains[(i, j)][0]
                solution.append(copy.deepcopy(sudoku_mat))

                modified += 1
    arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)

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
        #print('Mrv', MRV_Xind, MRV_Yind)
        mat = copy.deepcopy(sudoku_mat)
        while len(vaules) != 0:
            k = vaules.pop()
            p = []
            p.append(k)
            variables_domains.update({(MRV_Xind, MRV_Yind): p})

            #print(variables_domains[(i, j)])
            # arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
            k, v = backtracking(variables_domains, variables_arc_constraints, sudoku_mat, sol)
            if v == False:
                variables_domains = dm
                variables_arc_constraints = cst
                sudoku_mat = mat
                k = vaules.pop(0)
                variables_domains[(i, j)] = []
                variables_domains[(i, j)].append(k)
                sol = copy.deepcopy(solution)
            else:
                solution = v
                if is_complete(sudoku_mat):
                    return sudoku_mat, solution
                else:
                    pass
                    #print("tefgayhcdsjcsdmkc")
                    # backtracking(variables_domains, variables_arc_constraints, sudoku_mat)
        # variables_domains[(i, j)]=copy.deepcopy(vaules)
    else:
        arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
        if is_complete(sudoku_mat):
            return sudoku_mat, solution
        else:
            for i in range(0, 9):
                pass
                #print(sudoku_mat[i])
            # sleep(1)
            return backtracking(variables_domains, variables_arc_constraints, sudoku_mat, solution)

    arc_consistency(variables_domains, variables_arc_constraints, sudoku_mat)
    for i in range(0, 9):
        print(sudoku_mat[i])


def solve_sudoku(sudoku):
    variables_domains = {}
    variables_arc_constraints = {}
    initialize_variable_domains_and_constraints(variables_domains, variables_arc_constraints, sudoku)
    n = arc_consistency(variables_domains, variables_arc_constraints, sudoku.mat)
    # backtracking(variables_domains,variables_arc_constraints,sudoku.mat)
    _, v = backtracking(variables_domains, variables_arc_constraints, sudoku.mat, [copy.deepcopy(sudoku.mat)])
    return v

