import copy

import sudoku_logic
from app import CURRENT


def test_index_returns_sudoku_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_game_returns_puzzle_with_default_number_of_clues(client):
    response = client.get('/new')
    puzzle = response.get_json()['puzzle']

    assert response.status_code == 200
    assert len(puzzle) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in puzzle)
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 35
    assert CURRENT['solution'] is not None


def test_new_game_honors_clues_query_parameter(client):
    response = client.get('/new?clues=40')
    puzzle = response.get_json()['puzzle']

    assert response.status_code == 200
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 40


def test_check_solution_requires_an_active_game(client):
    response = client.post('/check', json={'board': sudoku_logic.create_empty_board()})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_solution_accepts_the_generated_solution(client):
    client.get('/new')
    response = client.post('/check', json={'board': copy.deepcopy(CURRENT['solution'])})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_solution_reports_incorrect_cells(client):
    client.get('/new')
    board = copy.deepcopy(CURRENT['solution'])
    board[0][0] = (board[0][0] % sudoku_logic.SIZE) + 1

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert [0, 0] in response.get_json()['incorrect']
