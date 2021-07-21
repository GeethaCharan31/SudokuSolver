import math

sudoku_board = [
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
size = len(sudoku_board)
cube_size = int(math.pow(size, 1 / 2))  # size of sub cube


def print_sudoku_board(board):
    for i in range(size):
        if i % cube_size == 0 and i != 0:
            print("-------------------")
        for j in range(size):
            if j % cube_size == 0 and j != 0:
                print("|", end="")
            print(board[i][j], end=" ")
        print()


def find_empty(board):
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return i, j
    return False


def is_valid(board, number, position):
    # checking row condition after inserting a number in a position(row,col)
    for i in range(size):
        if board[position[0]][i] == number and i != position[1]:
            return False
    # checking column condition
    for i in range(size):
        if board[i][position[1]] == number and i != position[0]:
            return False
    # checking cube condition
    # starting indices of cubes
    cube_row = (position[0] // cube_size) * cube_size
    cube_col = (position[1] // cube_size) * cube_size
    # traversing in cube
    for i in range(cube_row, cube_row + cube_size):
        for j in range(cube_col, cube_col + cube_size):
            if board[i][j] == number and (i, j) != position:
                return False
    return True


def solver(board):
    empty_slot = find_empty(board)
    if not empty_slot:
        return True
    else:
        row, col = empty_slot
        for i in range(1, size + 1):
            if is_valid(board, i, (row, col)):
                board[row][col] = i
                if solver(board):
                    return True
                board[row][col] = 0
        return False


solver(sudoku_board)
print_sudoku_board(sudoku_board)
