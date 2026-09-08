import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def _is_valid_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if value < 1 or value > SIZE:
                return False
            board[row][col] = EMPTY
            valid = is_safe(board, row, col, value)
            board[row][col] = value
            if not valid:
                return False
    return True

def _count_solutions(board, limit=2):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                count = 0
                for candidate in range(1, SIZE + 1):
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        count += _count_solutions(board, limit - count)
                        board[row][col] = EMPTY
                        if count >= limit:
                            return count
                return count
    return 1

def has_unique_solution(board):
    candidate = deep_copy(board)
    if not _is_valid_board(candidate):
        return False
    return _count_solutions(candidate, limit=2) == 1

def get_hint(puzzle, solution):
    for row in range(SIZE):
        for col in range(SIZE):
            if puzzle[row][col] == EMPTY:
                return {'row': row, 'col': col, 'value': solution[row][col]}
    return None

def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1

def generate_puzzle(clues=35):
    while True:
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        remove_cells(board, clues)
        puzzle = deep_copy(board)
        if has_unique_solution(puzzle):
            return puzzle, solution
