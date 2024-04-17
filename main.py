from gui import GUI
import queue
from random_sudoku_generator import Sudoku
from validator import isValidSudoku

N = 9
K = 40
sudoku = Sudoku(N, K)
sudoku.fillValues()
gui = GUI(sudoku.mat)

variables_domains = {}
variables_arc_constraints = {}
variables_that_require_consistency_enforcement = queue.Queue()


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
