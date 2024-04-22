import copy
import tkinter as tk
from tkinter import W, SUNKEN, RAISED
from tkinter.simpledialog import askstring
from random_sudoku_generator import Sudoku
from solver_with_arc_cons import solve_sudoku, print_mat


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
        self.current_board_solutions = None
        self.current_state = 1
        self.screen = tk.Tk()
        self.screen.title("Sudoku_w Board")
        self.screen.bind("<Key>", self.on_key_press)
        self.canvas = tk.Canvas(self.screen, width=1120, height=660)
        self.sudoku_canvas_objects = []
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_mouse_click)

        self.prefilled_cells = []

        self.mouse_x = None
        self.mouse_y = None
        self.selected_cell_row = None
        self.selected_cell_column = None
        self.cell_selected = False
        self.player_is_solving_puzzle = False
        self.hints_left = 3
        self.chances_left = 3
        self.player_displayed_stats_ids = {}
        self.agent_displayed_stats_ids = {}

        self.input_sudoku_matrix = None

        self.display_buttons()
        self.display_canvas(None)
        self.screen.mainloop()

    def display_canvas(self, matrix):
        for object_id in self.sudoku_canvas_objects:
            self.canvas.delete(object_id)
        self.display_sudoku(matrix)

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
        self.get_solution_button = tk.Button(self.screen, text="Get Solution", font=("Helvetica", 12, "bold"),
                                             width=get_solution_button_width, height=get_solution_button_height,
                                             activebackground="MediumOrchid3", background="bisque", borderwidth=2,
                                             command=self.get_solution_pressed)
        get_solution_button_window = self.canvas.create_window(get_solution_button_x, get_solution_button_y,
                                                               window=self.get_solution_button)

        solve_for_yourself_button_x = 884
        solve_for_yourself_button_y = 165
        solve_for_yourself_button_width = 43
        solve_for_yourself_button_height = 2
        self.solve_for_yourself_button = tk.Button(self.screen, text="Solve For Yourself",
                                                   font=("Helvetica", 12, "bold"),
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

        # player stats
        hints_label_x = 730
        hints_label_y = 240
        hints_label = tk.Label(self.screen, text="Hints left:", font=("Helvetica", 15, "bold"),
                               background="navajo white")
        hints_label_window = self.canvas.create_window(hints_label_x, hints_label_y, state="hidden", window=hints_label)
        self.player_displayed_stats_ids["hints_label_window"] = hints_label_window

        hints_data_label_x = 800
        hints_data_label_y = 240
        hints_data_label = tk.Label(self.screen, text=str(self.hints_left), font=("Helvetica", 15, "bold"),
                                    background="navajo white")
        hints_data_label_window = self.canvas.create_window(hints_data_label_x, hints_data_label_y, state="hidden",
                                                            window=hints_data_label)
        self.player_displayed_stats_ids["hints_data_label_window"] = hints_data_label_window

        chances_label_x = 745
        chances_label_y = 280
        chances_label = tk.Label(self.screen, text="Chances left:", font=("Helvetica", 15, "bold"),
                                 background="navajo white")
        chances_label_window = self.canvas.create_window(chances_label_x, chances_label_y, state="hidden",
                                                         window=chances_label)
        self.player_displayed_stats_ids["chances_label_window"] = chances_label_window

        chances_data_label_x = 830
        chances_data_label_y = 280
        chances_data_label = tk.Label(self.screen, text=str(self.chances_left), font=("Helvetica", 15, "bold"),
                                      background="navajo white")
        chances_data_label_window = self.canvas.create_window(chances_data_label_x, chances_data_label_y,
                                                              state="hidden",
                                                              window=chances_data_label)
        self.player_displayed_stats_ids["chances_data_label_window"] = chances_data_label_window

        state_label_x = 780
        state_label_y = 600
        state_label = tk.Label(self.screen, text="", font=("Helvetica", 15, "bold"), background="navajo white")
        state_label_window = self.canvas.create_window(state_label_x, state_label_y, state="hidden", window=state_label)
        self.agent_displayed_stats_ids["state_label_window"] = state_label_window

        back_button_x = 780
        back_button_y = 600
        back_button_width = 18
        back_button_height = 2
        back_button = tk.Button(self.screen, text="Back", font=("Helvetica", 12, "bold"),
                                width=back_button_width, height=back_button_height,
                                activebackground="MediumOrchid3", background="lemon chiffon", borderwidth=2,
                                command=self.back_pressed)
        back_button_window = self.canvas.create_window(back_button_x, back_button_y, state="hidden", window=back_button)
        self.agent_displayed_stats_ids["back_button_window"] = back_button_window

        next_button_x = 990
        next_button_y = 600
        next_button_width = 18
        next_button_height = 2
        next_button = tk.Button(self.screen, text="Next", font=("Helvetica", 12, "bold"),
                                width=next_button_width, height=next_button_height,
                                activebackground="MediumOrchid3", background="lemon chiffon", borderwidth=2,
                                command=self.next_pressed)
        next_button_window = self.canvas.create_window(next_button_x, next_button_y, state="hidden", window=next_button)
        self.agent_displayed_stats_ids["next_button_window"] = next_button_window

    def display_sudoku(self, matrix):
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
                    subsquare = get_subsquare(i, j, matrix)

                # Creating boxes in each sub square
                box_width = sub_container_width // 3
                box_height = sub_container_height // 3
                for m in range(3):
                    for n in range(3):
                        if m == 0:
                            if i == 0:
                                row = 0
                            elif i == 1:
                                row = 3
                            else:
                                row = 6
                        elif m == 1:
                            if i == 0:
                                row = 1
                            elif i == 1:
                                row = 4
                            else:
                                row = 7
                        else:
                            if i == 0:
                                row = 2
                            elif i == 1:
                                row = 5
                            else:
                                row = 8

                        if n == 0:
                            if j == 0:
                                column = 0
                            elif j == 1:
                                column = 3
                            else:
                                column = 6
                        elif n == 1:
                            if j == 0:
                                column = 1
                            elif j == 1:
                                column = 4
                            else:
                                column = 7
                        else:
                            if j == 0:
                                column = 2
                            elif j == 1:
                                column = 5
                            else:
                                column = 8

                        box_x = sub_container_x + n * box_width
                        box_y = sub_container_y + m * box_height

                        next_box_x = sub_container_x + (n + 1) * box_width
                        next_box_y = sub_container_y + (m + 1) * box_height

                        if self.player_is_solving_puzzle and self.mouse_x is not None and self.mouse_y is not None and box_x <= self.mouse_x <= next_box_x and box_y <= self.mouse_y <= next_box_y:
                            self.cell_selected = True
                            self.selected_cell_row = row
                            self.selected_cell_column = column
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

                            if (row, column) not in self.prefilled_cells:
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
        self.get_solution_button.config(relief=RAISED)
        self.current_board_solutions = None
        self.save_prefilled_cells()
        self.manage_player_stats("hide")
        self.manage_solution_stats("hide")
        self.display_canvas(self.board.mat)
        self.current_state = 1

    def collect_inputs(self):
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
            self.save_prefilled_cells()
            self.player_is_solving_puzzle = False
            self.solve_for_yourself_button.config(relief=RAISED)
            self.get_solution_button.config(relief=RAISED)
            self.current_board_solutions = None
            self.manage_player_stats("hide")
            self.manage_solution_stats("hide")
            self.display_canvas(self.board.mat)
            self.current_state = 1

        # Create a button to submit the inputs and call the function
        submit_button = tk.Button(input_window, text="Save", command=save_input)
        submit_button.pack(pady=10)

        # Start the main loop of the top-level window
        input_window.mainloop()

    def on_mouse_click(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.cell_selected = False
        self.display_canvas(self.board.mat)

    def on_key_press(self, event):
        print(event.char)
        if not self.cell_selected:
            return
        if self.board.mat[self.selected_cell_row][self.selected_cell_column] == 0:
            if event.char.isdigit() and 1 <= int(event.char) <= 9:
                print(self.selected_cell_row, self.selected_cell_column)
                self.board.mat[self.selected_cell_row][self.selected_cell_column] = int(event.char)
                self.display_canvas(self.board.mat)

    def manage_solution_stats(self, command):
        if command == "show":
            for key, value in self.agent_displayed_stats_ids.items():
                self.canvas.itemconfig(value, state="normal")

        else:
            for _, value in self.agent_displayed_stats_ids.items():
                self.canvas.itemconfig(value, state="hidden")

    def manage_player_stats(self, command):
        if command == "show":
            for _, value in self.player_displayed_stats_ids.items():
                self.canvas.itemconfig(value, state="normal")
        else:
            for _, value in self.player_displayed_stats_ids.items():
                self.canvas.itemconfig(value, state="hidden")

    def get_solution_pressed(self):
        if self.current_board_solutions is None:
            self.current_board_solutions = solve_sudoku(copy.deepcopy(self.board))
        print(self.current_board_solutions[-1])
        print(self.board.mat)
        self.manage_solution_stats("show")
        self.manage_player_stats("hide")
        self.get_solution_button.config(relief=SUNKEN)
        self.player_is_solving_puzzle = False
        self.solve_for_yourself_button.config(relief=RAISED)

    def solve_for_yourself_pressed(self):
        if self.board is not None:
            self.hints_left = 3
            self.chances_left = 3
            self.player_is_solving_puzzle = True
            self.solve_for_yourself_button.config(relief=SUNKEN)
            self.get_solution_button.config(relief=RAISED)
            self.manage_player_stats("show")
            self.manage_solution_stats("hide")
            self.display_canvas(self.board.mat)

    def back_pressed(self):
        if self.current_state > 1:
            self.current_state -= 1
            self.display_canvas(self.current_board_solutions[self.current_state - 1])

    def next_pressed(self):
        if self.current_state < len(self.current_board_solutions):
            self.current_state += 1
            self.display_canvas(self.current_board_solutions[self.current_state - 1])

    def save_prefilled_cells(self):
        self.prefilled_cells.clear()
        for i in range(9):
            for j in range(9):
                if self.board.mat[i][j] != 0:
                    self.prefilled_cells.append((i, j))
        print(self.prefilled_cells)
