import pygame.display

from cell import Cell
from sudokusolver import find_empty, is_valid, solve


class Grid:
    grid1 = [
        [0, 6, 0, 1, 0, 4, 0, 5, 0],
        [0, 0, 8, 3, 0, 5, 6, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 1],
        [8, 0, 0, 4, 0, 7, 0, 0, 6],
        [0, 0, 6, 0, 0, 0, 3, 0, 0],
        [7, 0, 0, 9, 0, 1, 0, 0, 4],
        [5, 0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 7, 2, 0, 6, 9, 0, 0],
        [0, 4, 0, 5, 0, 8, 0, 7, 0]
    ]
    grid2 = [
        [3, 0, 6, 5, 0, 8, 4, 0, 0],
        [5, 2, 0, 0, 0, 0, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 3, 1],
        [0, 0, 3, 0, 1, 0, 0, 8, 0],
        [9, 0, 0, 8, 6, 3, 0, 0, 5],
        [0, 5, 0, 0, 9, 0, 6, 0, 0],
        [1, 3, 0, 0, 0, 0, 2, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 7, 4],
        [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]
    grid3 = [
        [0, 6, 2, 3, 0, 8, 4, 0, 0],
        [1, 8, 5, 0, 2, 0, 7, 0, 3],
        [0, 7, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 3, 9, 6],
        [0, 9, 0, 0, 0, 0, 1, 0, 7],
        [7, 0, 0, 0, 9, 6, 2, 8, 0],
        [5, 3, 1, 9, 0, 0, 6, 0, 0],
        [0, 4, 9, 0, 5, 0, 0, 0, 1],
        [0, 2, 0, 6, 0, 0, 0, 4, 0]

    ]
    grid4 = [
        [9, 6, 2, 3, 7, 8, 4, 1, 5],
        [1, 8, 5, 4, 2, 9, 7, 6, 3],
        [3, 7, 4, 5, 6, 1, 9, 2, 8],
        [2, 1, 8, 7, 4, 5, 3, 9, 6],
        [0, 9, 6, 8, 3, 2, 1, 5, 7],
        [7, 5, 3, 1, 9, 6, 2, 8, 4],
        [5, 3, 1, 9, 8, 4, 6, 7, 2],
        [6, 4, 9, 2, 5, 7, 8, 3, 1],
        [8, 2, 7, 6, 1, 3, 5, 4, 9]

    ]
    board = grid4

    def __init__(self, rows, cols, width, height, win, dm):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.win = win

        self.cells = None
        self.make_cells()

        self.model = None
        self.update_model()

        self.selected = None
        self.dm = dm

    def make_cells(self):
        """create cell objects"""
        self.cells = [[Cell(self.board[i][j], i, j, self.width, self.height) for j in range(self.cols)] for i
                      in
                      range(self.rows)]

    def update_model(self):
        """to update the model"""
        self.model = [[self.cells[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        """place value into cell only if its correct"""
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_value(val)
            self.update_model()

            if is_valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cells[row][col].set_value(0)
                self.cells[row][col].set_temp(0)
                self.update_model()
                return False

    def clear_cell(self):
        """to clear the cell when del is pressed """
        row, col = self.selected
        if self.cells[row][col].value == 0:
            self.cells[row][col].set_temp(0)

    def solve_gui(self):
        """solver function for gui"""
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if is_valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cells[row][col].set_value(i)
                self.cells[row][col].draw_changes(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(10)

                if self.solve_gui():
                    return True

                self.model[row][col] = 0
                self.cells[row][col].set_value(0)
                self.update_model()
                self.cells[row][col].draw_changes(self.win, False)
                pygame.display.update()
                pygame.time.delay(10)

        return False

    def is_finished(self):
        """to check whether all cells are filled"""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cells[i][j].value == 0:
                    return False
        return True

    def click(self, position):
        """returns the (row,col) of the cell"""
        if position[0] < self.width and position[1] < self.height:
            gap = self.width / 9
            x = position[0] // gap
            y = position[1] // gap
            return int(y), int(x)
        else:
            return None

    def select_cell(self, row, col):
        """select a cell and also deselect all"""
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].selected = False

        self.cells[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, val):
        row, col = self.selected
        self.cells[row][col].set_temp(val)

    def draw(self):
        if self.dm.get_mode():
            line_color = (255, 255, 255)
        else:
            line_color = (0, 0, 0)
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, line_color, (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, line_color, (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cells[i][j].draw(self.win)
