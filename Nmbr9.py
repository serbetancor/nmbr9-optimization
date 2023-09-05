import tkinter as tk

class Nmbr9GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Nmbr9 Solver")

        self.board_size = 15
        self.cell_size = 30
        self.canvas_width = self.board_size * self.cell_size + 40
        self.canvas_height = self.board_size * self.cell_size + 40  # Extra space for number buttons

        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Define colors and shapes for each number
        self.number_info = {
            0: (("#cecbb9"), [[1, 1, 1], [1, 0, 1], [1, 0, 1], [1, 1, 1]]),
            1: (("#caae84"), [[1, 1], [0, 1], [0, 1], [0, 1]]),
            2: (("#ffc56d"), [[0, 1, 1], [0, 1, 1], [1, 1, 0], [1, 1, 1]]),
            3: (("#fff88f"), [[1, 1, 1], [0, 0, 1], [0, 1, 1], [1, 1, 1]]),
            4: (("#a5e196"), [[0, 1, 1], [0, 1, 0], [1, 1, 1], [0, 1, 1]]),
            5: (("#ace2da"), [[1, 1, 1], [1, 1, 1], [0, 0, 1], [1, 1, 1]]),
            6: (("#81bfff"), [[1, 1, 0], [1, 0, 0], [1, 1, 1], [1, 1, 1]]),
            7: (("#f290da"), [[1, 1, 1], [0, 1, 0], [1, 1, 0], [1, 0, 0]]),
            8: (("#fbc0e0"), [[0, 1, 1], [0, 1, 1], [1, 1, 0], [1, 1, 0]]),
            9: (("#ff7e67"), [[1, 1, 1], [1, 1, 1], [1, 1, 0], [1, 1, 0]])
            # Define shapes and colors for other numbers
            # ...
        }

        self.placed_numbers = [[0] * self.board_size for _ in range(self.board_size)]
        self.selected_number = None

        self.unavailable_positions = set()  # Set to keep track of occupied positions

        self.create_board_gui()
        self.create_number_buttons()
        self.create_reset_button()

    def create_board_gui(self):
        margin = 10

        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * self.cell_size + margin
                y1 = row * self.cell_size + margin
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                self.canvas.create_rectangle(x1, y1, x2, y2)

    def draw_number(self, row, col, color, shape):
        for r, row_shape in enumerate(shape):
            for c, cell_value in enumerate(row_shape):
                if cell_value == 1:
                    cell_row = row - len(shape) // 2 + r
                    cell_col = col - len(row_shape) // 2 + c
                    if 0 <= cell_row < self.board_size and 0 <= cell_col < self.board_size:
                        self.color_cell(cell_row, cell_col, color)

    def color_cell(self, row, col, color):
        cell_x1 = col * self.cell_size + 10  # Add margin
        cell_y1 = row * self.cell_size + 10  # Add margin
        cell_x2 = cell_x1 + self.cell_size
        cell_y2 = cell_y1 + self.cell_size
        self.canvas.create_rectangle(cell_x1, cell_y1, cell_x2, cell_y2, fill=color)

    def create_number_buttons(self):
        number_frame = tk.Frame(self.root)
        number_frame.pack(pady=10)

        for number in range(10):
            number_button = tk.Button(number_frame, text=str(number), width=3, command=lambda n=number: self.on_number_button_click(n))
            number_button.pack(side=tk.LEFT, padx=5)

    def on_number_button_click(self, number):
        
        self.selected_number = number

        center_row = self.board_size // 2
        center_col = self.board_size // 2

        if self.placed_numbers[center_row][center_col] == 0:
            if self.can_place_number(center_row, center_col, self.number_info[self.selected_number][1]):
                self.place_number(center_row, center_col)
        else:
            valid_placements = []

            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.can_place_number(row, col, self.number_info[self.selected_number][1]):
                        valid_placements.append((row, col))

            if valid_placements:
                row, col = self.find_available_position(valid_placements)
                self.place_number(row, col)
                
        print(self.number_info[self.selected_number][1])
        print(self.unavailable_positions)


    def find_available_position(self, valid_placements):
        for row, col in valid_placements:
            shape = self.number_info[self.selected_number][1]
            is_available = True

            for r, row_shape in enumerate(shape):
                for c, cell_value in enumerate(row_shape):
                    if cell_value == 1:
                        cell_row = row - len(shape) // 2 + r
                        cell_col = col - len(row_shape) // 2 + c
                        if (cell_row, cell_col) in self.unavailable_positions:
                            is_available = False
                            break

                if not is_available:
                    break

            if is_available:
                return row, col

        return valid_placements[0]  # If no available position found, use the first valid placement


    def place_number(self, row, col):
        color, shape = self.number_info[self.selected_number]
        self.draw_number(row, col, color, shape)

        for r, row_shape in enumerate(shape):
            for c, cell_value in enumerate(row_shape):
                if cell_value == 1:
                    cell_row = row - len(shape) // 2 + r
                    cell_col = col - len(row_shape) // 2 + c
                    self.unavailable_positions.add((cell_row, cell_col))
                    self.placed_numbers[cell_row][cell_col] = self.selected_number

    def can_place_number(self, row, col, shape):
        for r, row_shape in enumerate(shape):
            for c, cell_value in enumerate(row_shape):
                if cell_value == 1:
                    cell_row = row - len(shape) // 2 + r
                    cell_col = col - len(row_shape) // 2 + c
                    if (
                        cell_row < 0
                        or cell_col < 0
                        or cell_row >= self.board_size
                        or cell_col >= self.board_size
                        or self.placed_numbers[cell_row][cell_col] != 0
                    ):
                        return False
        return True

    
    def create_reset_button(self):
        reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        reset_button.pack()

    def reset_board(self):
        self.placed_numbers = [[0] * self.board_size for _ in range(self.board_size)]
        self.selected_number = None
        self.unavailable_positions = set()
        self.canvas.delete("all")
        self.create_board_gui()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x800")  # Adjust the size as needed
    nmbr9_gui = Nmbr9GUI(root)
    nmbr9_gui.run()
