import random


#check if a number can be placed in a cell without violating constraints
def is_valid_placement(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


def solve_sudoku(board):
    def backtrack(row=0, col=0):
        if col == 9:
            row += 1
            col = 0
            if row == 9:
                return board  #Solved
        if board[row][col] != 0:
            return backtrack(row, col + 1)

        for num in range(1, 10):
            if is_valid_placement(board, row, col, num):
                board[row][col] = num
                solution = backtrack(row, col + 1)
                if solution is not None:
                    return solution
                board[row][col] = 0  #Backtrack

        return None  #No solution

    solution = backtrack()
    return solution


#check if a partially filled board can be solved
def is_solvable(board):

    #check row and column constraints
    for i in range(9):
        row_numbers = set()
        col_numbers = set()
        for j in range(9):
            if board[i][j] != 0:
                if board[i][j] in row_numbers or board[j][i] in col_numbers:
                    return False
                row_numbers.add(board[i][j])
                col_numbers.add(board[j][i])

    #check subgrid constraints
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid_numbers = set()
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    if board[k][l] != 0 and board[k][l] in subgrid_numbers:
                        return False
                    subgrid_numbers.add(board[k][l])

    return True


def generate_puzzle():

    #generate a complete Sudoku solution
    def generate_solution():
        board = [[0 for _ in range(9)] for _ in range(9)]
        solve_sudoku(board)
        return board

    #remove numbers while keeping the puzzle solvable
    def remove_numbers(board, difficulty):
        # Determine the number of cells to remove based on difficulty
        if difficulty == "easy":
            cells_to_remove = 30
        elif difficulty == "medium":
            cells_to_remove = 40
        else:
            cells_to_remove = 50

        #randomly select cells to remove while ensuring the puzzle remains solvable
        for _ in range(cells_to_remove):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            removed_number = board[row][col]
            board[row][col] = 0
            #check if the puzzle remains solvable after removing the number
            temp_board = [row[:] for row in board]
            if not is_solvable(temp_board):
                board[row][col] = removed_number  #restore the removed number

    solution = generate_solution()
    puzzle = [row[:] for row in solution]  #create a copy of the solution as the puzzle
    remove_numbers(puzzle, "medium")  #adjust difficulty as needed
    return puzzle


def print_board(board):
    for row in board:
        print(row)


def test_solve_sudoku():

    puzz = generate_puzzle()
    print("puzzle before solution:")
    print_board(puzz)
    solution1 = solve_sudoku(puzz)
    print("Solution 1:")
    print_board(solution1)


if __name__ == "__main__":
    test_solve_sudoku()
