import random
import copy


def is_valid_place(board, row, col, num):
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


def solver(board):
    def backtrack(row=0, col=0):
        if col == 9:
            row += 1
            col = 0
            if row == 9:
                return board  #solved
        if board[row][col] != 0:
            return backtrack(row, col + 1)

        numbers = list(range(1, 10))
        random.shuffle(numbers)
        for _ in range(9):
            num = numbers.pop()
            if is_valid_place(board, row, col, num):
                board[row][col] = num
                solution = backtrack(row, col + 1)
                if solution is not None:
                    return solution
                board[row][col] = 0  # backtrack

        return None  #no solution

    solution = backtrack()
    return solution


def is_solvable(board):

    # check row and column constraints
    for i in range(9):
        row_nums = set()
        col_nums = set()
        for j in range(9):
            if board[i][j] != 0:
                if board[i][j] in row_nums or board[j][i] in col_nums:
                    return False
                row_nums.add(board[i][j])
                col_nums.add(board[j][i])

    # check subgrid constraints
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            subgrid_nums = set()
            for k in range(i, i + 3):
                for l in range(j, j + 3):
                    if board[k][l] != 0 and board[k][l] in subgrid_nums:
                        return False
                    subgrid_nums.add(board[k][l])

    return True


def generate_puzzle(difficulty):

    # generate a complete sudoku solution
    def generate_solution():
        board = [[0 for _ in range(9)] for _ in range(9)]
        solver(board)
        return board

    def remove_numbers(board, diff):
        # Determine the number of cells to remove based on difficulty
        if diff == "Easy":
            removedCells = 38
        elif diff == "Medium":
            removedCells = 47
        else:
            removedCells = 56

        # randomly select cells to remove while ensuring the puzzle remains solvable
        for _ in range(removedCells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
           # removed_number = board[row][col]
            board[row][col] = 0
            # check if the puzzle remains solvable after removing the number
            #currentState = copy.deepcopy(board)
            #if not is_solvable(currentState):
             #   board[row][col] = removed_number  # restore the removed number

    solution = generate_solution()
    puzzle = [row[:] for row in solution]
    remove_numbers(puzzle, difficulty)  # pass the difficulty level
    return puzzle


def print_board(board):
    for row in board:
        print(row)


def test_solver():

    puzz = generate_puzzle("M")
    print("puzzle before solution:")
    print_board(puzz)
    solution1 = solver(puzz)
    print("Solution 1:")
    print_board(solution1)


if __name__ == "__main__":
    test_solver()
