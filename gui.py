import tkinter as tk
from tkinter import W, SUNKEN, RAISED
from tkinter.simpledialog import askstring

from random_sudoku_generator import Sudoku


def get_subsquare(i, j, matrix):
    row_start = i * 3
    column_start = j * 3
    square = [[], [], []]

    m = row_start
    n = column_start

    for i in range(3):
        for j in range(3):
            square[i].append(matrix[m][n])
            n += 1
        m += 1
        n = column_start
    return square


def get_sudoku_input():
    # Initialize a list to store the collected inputs
    inputs = []

    # Define the prompts to ask the user
    prompts = ['What is your name?', 'What is your age?', 'What is your favorite color?']

    # Iterate through the prompts and ask the user for input
    for prompt in prompts:
        response = askstring('Input Required', prompt)
        if response is not None:
            inputs.append(response)

    # Display all the collected inputs in a single message box
    info_message = "\n".join(inputs)
    print('Collected Inputs', info_message)


class GUI:
    def __init__(self):
        self.N = 9
        self.K = 40
        self.board = None
        self.screen = tk.Tk()
        self.screen.title("Sudoku_w Board")
        self.screen.bind("<Key>", self.on_key_press)
        self.canvas = tk.Canvas(self.screen, width=1120, height=660)
        self.sudoku_canvas_objects = []
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_mouse_click)

        self.mouse_x = None
        self.mouse_y = None
        self.selected_cell_row = None
        self.selected_cell_column = None
        self.cell_selected = False
        self.player_is_solving_puzzle = False

        self.input_sudoku_matrix = None

        self.display_buttons()
        self.display_canvas()
        self.screen.mainloop()

    def display_canvas(self, newly_filled_cell_row=None, newly_filled_cell_column=None):
        for object_id in self.sudoku_canvas_objects:
            self.canvas.delete(object_id)
        self.display_sudoku(newly_filled_cell_row, newly_filled_cell_column)

    def display_buttons(self):
        # Create input sudoku, generate sudoku, get solution, solve for yourself buttons
        input_sudoku_button_x = 770
        input_sudoku_button_y = 45
        input_sudoku_button_width = 20
        input_sudoku_button_height = 2
        input_sudoku_button = tk.Button(self.screen, text="Input Sudoku", font=("Helvetica", 12, "bold"),
                                        width=input_sudoku_button_width, height=input_sudoku_button_height,
                                        activebackground="MediumOrchid3", background="papaya whip",
                                        borderwidth=2, command=self.collect_inputs)
        input_sudoku_button_window = self.canvas.create_window(input_sudoku_button_x, input_sudoku_button_y,
                                                               window=input_sudoku_button)

        generate_sudoku_button_x = 1000
        generate_sudoku_button_y = 45
        generate_sudoku_button_width = 20
        generate_sudoku_button_height = 2
        generate_sudoku_button = tk.Button(self.screen, text="Generate Sudoku", font=("Helvetica", 12, "bold"),
                                           width=generate_sudoku_button_width, height=generate_sudoku_button_height,
                                           activebackground="MediumOrchid3", background="blanched almond",
                                           borderwidth=2, command=self.generate_random_sudoku)
        generate_sudoku_button_window = self.canvas.create_window(generate_sudoku_button_x, generate_sudoku_button_y,
                                                                  window=generate_sudoku_button)

        get_solution_button_x = 884
        get_solution_button_y = 105
        get_solution_button_width = 43
        get_solution_button_height = 2
        get_solution_button = tk.Button(self.screen, text="Get Solution", font=("Helvetica", 12, "bold"),
                                        width=get_solution_button_width, height=get_solution_button_height,
                                        activebackground="MediumOrchid3",
                                        background="bisque", borderwidth=2)
        get_solution_button_window = self.canvas.create_window(get_solution_button_x, get_solution_button_y,
                                                               window=get_solution_button)

        solve_for_yourself_button_x = 884
        solve_for_yourself_button_y = 165
        solve_for_yourself_button_width = 43
        solve_for_yourself_button_height = 2
        self.solve_for_yourself_button = tk.Button(self.screen, text="Solve For Yourself", font=("Helvetica", 12, "bold"),
                                              width=solve_for_yourself_button_width,
                                              height=solve_for_yourself_button_height,
                                              activebackground="MediumOrchid3", background="peach puff",
                                              borderwidth=2, command=self.solve_for_yourself_pressed)
        solve_for_yourself_button_window = self.canvas.create_window(solve_for_yourself_button_x,
                                                                     solve_for_yourself_button_y,
                                                                     window=self.solve_for_yourself_button)

        # Create container for notes and back, next buttons
        notes_container_x = 665
        notes_container_y = 200
        notes_container_width = 438
        notes_container_height = 450
        self.canvas.create_rectangle(notes_container_x, notes_container_y, notes_container_x + notes_container_width,
                                     notes_container_y + notes_container_height,
                                     outline="black", width=2, fill="navajo white")

        back_button_x = 780
        back_button_y = 600
        back_button_width = 18
        back_button_height = 2
        back_button = tk.Button(self.screen, text="Back", font=("Helvetica", 12, "bold"),
                                width=back_button_width, height=back_button_height,
                                activebackground="MediumOrchid3", background="lemon chiffon", borderwidth=2)
        back_button_window = self.canvas.create_window(back_button_x, back_button_y, window=back_button)

        next_button_x = 990
        next_button_y = 600
        next_button_width = 18
        next_button_height = 2
        next_button = tk.Button(self.screen, text="Next", font=("Helvetica", 12, "bold"),
                                width=next_button_width, height=next_button_height,
                                activebackground="MediumOrchid3", background="lemon chiffon", borderwidth=2)
        next_button_window = self.canvas.create_window(next_button_x, next_button_y, window=next_button)

    def display_sudoku(self, newly_filled_cell_row=None, newly_filled_cell_column=None):
        # Create main Sudoku container
        container_x = 20
        container_y = 20
        container_width = 630
        container_height = 630
        self.sudoku_canvas_objects.append(
            self.canvas.create_rectangle(container_x, container_y, container_x + container_width,
                                         container_y + container_height,
                                         outline="black", width=6, fill="antique white"))

        # Create containers for all 9 sub-squares
        sub_container_width = container_width // 3
        sub_container_height = container_height // 3
        for i in range(3):
            for j in range(3):
                sub_container_x = container_x + j * sub_container_width
                sub_container_y = container_y + i * sub_container_height
                self.sudoku_canvas_objects.append(self.canvas.create_rectangle(sub_container_x, sub_container_y,
                                                                               sub_container_x + sub_container_width,
                                                                               sub_container_y + sub_container_height,
                                                                               outline="black", width=6,
                                                                               fill="antique white"))

                if self.board is not None:
                    subsquare = get_subsquare(i, j, self.board.mat)

                # Creating boxes in each sub square
                box_width = sub_container_width // 3
                box_height = sub_container_height // 3
                for m in range(3):
                    for n in range(3):
                        box_x = sub_container_x + n * box_width
                        box_y = sub_container_y + m * box_height

                        next_box_x = sub_container_x + (n + 1) * box_width
                        next_box_y = sub_container_y + (m + 1) * box_height

                        if self.player_is_solving_puzzle and self.mouse_x is not None and self.mouse_y is not None and box_x <= self.mouse_x <= next_box_x and box_y <= self.mouse_y <= next_box_y:
                            self.cell_selected = True
                            self.selected_cell_row = m
                            self.selected_cell_column = n
                            self.sudoku_canvas_objects.append(
                                self.canvas.create_rectangle(box_x, box_y, box_x + box_width, box_y + box_height,
                                                             outline="black", width=1, fill="NavajoWhite2"))
                        else:
                            self.sudoku_canvas_objects.append(
                                self.canvas.create_rectangle(box_x, box_y, box_x + box_width, box_y + box_height,
                                                             outline="black", width=1, fill="antique white"))

                        if self.board is not None and subsquare[m][n] != 0:
                            text_x = box_x + box_width / 2
                            text_y = box_y + box_height / 2
                            if m == newly_filled_cell_row and n == newly_filled_cell_column:
                                self.sudoku_canvas_objects.append(
                                    self.canvas.create_text(text_x, text_y, text=str(subsquare[m][n]),
                                                            font=("Helvetica", 35, "bold"),
                                                            fill="blue"))
                            else:
                                self.sudoku_canvas_objects.append(
                                    self.canvas.create_text(text_x, text_y, text=str(subsquare[m][n]),
                                                            font=("Helvetica", 35, "bold"),
                                                            fill="black"))

    def generate_random_sudoku(self):
        self.board = Sudoku(self.N, self.K)
        self.board.fillValues()
        self.player_is_solving_puzzle = False
        self.solve_for_yourself_button.config(relief=RAISED)
        self.display_canvas()

    def collect_inputs(self):
        self.player_is_solving_puzzle = False
        self.solve_for_yourself_button.config(relief=RAISED)
        # Create a new top-level window for collecting inputs
        input_window = tk.Toplevel(self.screen)
        input_window.title("Input Sudoku Format")
        input_window.geometry("300x250")

        # Initialize a list to store the questions and corresponding entries
        prompts = ['row 1', 'row 2', 'row 3', 'row 4', 'row 5', 'row 6', 'row 7', 'row 8', 'row 9']
        entries = []

        # Create a frame to hold the prompts and entries
        frame = tk.Frame(input_window)
        frame.pack(padx=10, pady=10)

        # Iterate through the prompts and create labels and entries
        for i, question in enumerate(prompts):
            label = tk.Label(frame, text=question)
            label.grid(row=i, column=0, sticky=W)
            entry = tk.Entry(frame, width=30)
            entry.grid(row=i, column=1)
            entries.append(entry)

        # Define a function to retrieve the inputs and show the result
        def save_input():
            self.input_sudoku_matrix = []
            rows = [entry.get() for entry in entries]
            for row in rows:
                matrix_row = []
                for char in row:
                    matrix_row.append(int(char))
                self.input_sudoku_matrix.append(matrix_row)
            input_window.destroy()
            self.board = Sudoku(self.N, self.K)
            self.board.mat = self.input_sudoku_matrix
            self.display_canvas()

        # Create a button to submit the inputs and call the function
        submit_button = tk.Button(input_window, text="Save", command=save_input)
        submit_button.pack(pady=10)

        # Start the main loop of the top-level window
        input_window.mainloop()

    def on_mouse_click(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.cell_selected = False
        self.display_canvas()

    def on_key_press(self, event):
        print(event.char)
        if not self.cell_selected:
            return
        if self.board.mat[self.selected_cell_row][self.selected_cell_column] == 0:
            if event.char.isdigit() and 1 <= int(event.char) <= 9:
                print(self.selected_cell_row, self.selected_cell_column)
                self.board.mat[self.selected_cell_row][self.selected_cell_column] = int(event.char)
                self.display_canvas(self.selected_cell_row, self.selected_cell_column)

    def solve_for_yourself_pressed(self):
        self.player_is_solving_puzzle = True
        self.solve_for_yourself_button.config(relief=SUNKEN)
