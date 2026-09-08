import sudoku_logic


def test_create_empty_board_has_nine_rows_of_nine_zeroes():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_does_not_share_nested_rows():
    board = sudoku_logic.create_empty_board()
    copied_board = sudoku_logic.deep_copy(board)

    copied_board[0][0] = 9

    assert board[0][0] == sudoku_logic.EMPTY
    assert copied_board[0][0] == 9


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 4) is True


def test_fill_board_creates_a_complete_valid_solution():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in board)
    assert all(
        sorted(board[row][col] for row in range(sudoku_logic.SIZE))
        == list(range(1, sudoku_logic.SIZE + 1))
        for col in range(sudoku_logic.SIZE)
    )


def test_has_unique_solution_accepts_a_completed_board():
    board = sudoku_logic.create_empty_board()
    sudoku_logic.fill_board(board)

    assert sudoku_logic.has_unique_solution(board) is True


def test_has_unique_solution_rejects_a_board_with_multiple_solutions():
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.has_unique_solution(board) is False


def test_has_unique_solution_rejects_invalid_board():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert sudoku_logic.has_unique_solution(board) is False


def test_generate_puzzle_returns_solution_and_requested_number_of_clues():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert all(
        puzzle[row][col] in (sudoku_logic.EMPTY, solution[row][col])
        for row in range(sudoku_logic.SIZE)
        for col in range(sudoku_logic.SIZE)
    )
    assert all(sorted(row) == list(range(1, sudoku_logic.SIZE + 1)) for row in solution)
    assert sudoku_logic.has_unique_solution(puzzle) is True
