from gui import GUI
from random_sudoku_generator import Sudoku

N = 9
K = 40
sudoku = Sudoku(N, K)
sudoku.fillValues()
sudoku.printSudoku()
gui = GUI(sudoku.mat)
