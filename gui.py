import tkinter as tk


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


class GUI:
    def __init__(self, sudoku_board):
        self.board = sudoku_board
        self.screen = tk.Tk()
        self.screen.title("Sudoku_w Board")
        self.canvas = tk.Canvas(self.screen, width=800, height=800)

        # Create main Sudoku_w container
        container_x = 100
        container_y = 100
        container_width = 630
        container_height = 630
        self.canvas.create_rectangle(container_x, container_y, container_x + container_width,
                                     container_y + container_height,
                                     outline="black", width=6, fill="beige")

        # Create containers for all 9 sub-squares
        sub_container_width = container_width // 3
        sub_container_height = container_height // 3
        for i in range(3):
            for j in range(3):
                sub_container_x = container_x + j * sub_container_width
                sub_container_y = container_y + i * sub_container_height
                self.canvas.create_rectangle(sub_container_x, sub_container_y, sub_container_x + sub_container_width,
                                             sub_container_y + sub_container_height, outline="black", width=6,
                                             fill="beige")

                subsquare = get_subsquare(i, j, self.board)

                # Creating boxes in each sub square
                box_width = sub_container_width // 3
                box_height = sub_container_height // 3
                for m in range(3):
                    for n in range(3):
                        box_x = sub_container_x + n * box_width
                        box_y = sub_container_y + m * box_height
                        self.canvas.create_rectangle(box_x, box_y, box_x + box_width, box_y + box_height,
                                                     outline="black", width=1, fill="beige")
                        if subsquare[m][n] != 0:
                            text_x = box_x + box_width / 2
                            text_y = box_y + box_height / 2
                            self.canvas.create_text(text_x, text_y, text=str(subsquare[m][n]),
                                                    font=("Helvetica", 35, "bold"),
                                                    fill="black")

        self.canvas.pack()
        self.screen.mainloop()
