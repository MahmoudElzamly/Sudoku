import random


# Function to check if placing a number at a certain position is valid
def is_valid_place(board, row, col, num):
    # Check if the number already exists in the same row or column
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    # Check if the number already exists in the same row or column
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    # Check if the number already exists in the 3x3 subgrid
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True


# Function to solve the Sudoku puzzle using backtracking
def solver(board):
    def backtrack(row=0, col=0):
        # If reached the end of the column, move to the next row
        if col == 9:
            row += 1
            col = 0
        # If reached the end of the board, the puzzle is solved
            if row == 9:
                return board  # solved
        # If the cell is already filled, move to the next cell
        if board[row][col] != 0:
            return backtrack(row, col + 1)
        # Generate random numbers from 1 to 9
        numbers = list(range(1, 10))
        random.shuffle(numbers)
        # Try each number
        for _ in range(9):
            num = numbers.pop()
            # If the number is valid, fill the cell with the number and try to solve the rest of the puzzle
            if is_valid_place(board, row, col, num):
                board[row][col] = num
                solution = backtrack(row, col + 1)
                if solution is not None:
                    return solution
                # If no solution found with this number, backtrack by setting the cell to 0
                board[row][col] = 0  # backtrack

        return None  # no solution

    solution = backtrack()
    return solution


# Function to generate a Sudoku puzzle with specified difficulty level
def generate_puzzle(difficulty):
    # generate a complete sudoku solution
    def generate_solution():
        board = [[0 for _ in range(9)] for _ in range(9)]
        solver(board)
        return board

    # Function to remove numbers from the solution based on difficulty level
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
            board[row][col] = 0

    # Calls
    solution = generate_solution()
    puzzle = [row[:] for row in solution]
    remove_numbers(puzzle, difficulty)  # pass the difficulty level
    return puzzle


def print_board(board):
    for row in board:
        print(row)


def test_solver():
    puzz = [[2, 0, 0, 0, 9, 0, 0, 4, 5],
            [0, 9, 0, 0, 5, 1, 8, 0, 2],
            [7, 5, 0, 4, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3, 0, 8],
            [1, 0, 0, 3, 6, 7, 4, 0, 0],
            [0, 7, 4, 8, 0, 0, 0, 0, 1],
            [5, 3, 1, 2, 0, 6, 0, 0, 4],
            [8, 2, 0, 9, 4, 5, 6, 0, 3],
            [0, 4, 0, 0, 0, 8, 0, 0, 0]]
    puzzle = generate_puzzle("M")
   # print("puzzle before solution:")
    # print_board(puzz)

# solution1 = solver(puzz)
# print("Solution 1:")
# print_board(solution1)


if __name__ == "__main__":
    test_solver()
