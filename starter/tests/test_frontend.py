from pathlib import Path


MAIN_JS = Path(__file__).parents[1] / 'static' / 'main.js'


def test_frontend_defines_top_ten_local_storage_flow():
    source = MAIN_JS.read_text()

    assert "const LEADERBOARD_KEY = 'sudokuLeaderboard';" in source
    assert 'function loadScores()' in source
    assert 'function saveScores(scores)' in source
    assert 'function recordScore(name, time, difficulty)' in source
    assert 'slice(0, MAX_SCORES)' in source


def test_frontend_records_scores_after_a_successful_timed_game():
    source = MAIN_JS.read_text()

    assert 'startTimer();' in source
    assert 'stopTimer();' in source
    assert "window.prompt('Enter your name for the Top 10 leaderboard:')" in source
    assert 'recordScore(name, elapsed, settings.label);' in source
    assert 'renderLeaderboard();' in source


def test_frontend_hint_locks_one_returned_cell_and_check_skips_locked_cells():
    source = MAIN_JS.read_text()

    assert "fetch('/hint')" in source
    assert 'input.disabled = true;' in source
    assert "input.className = 'sudoku-cell hinted';" in source
    assert 'if (inp.disabled) continue;' in source


def test_frontend_persists_and_applies_selected_theme():
    source = MAIN_JS.read_text()

    assert "const THEME_KEY = 'sudokuTheme';" in source
    assert 'function applyTheme(theme)' in source
    assert 'function loadTheme()' in source
    assert 'function toggleTheme()' in source
    assert "document.documentElement.dataset.theme = selectedTheme;" in source
    assert "localStorage.setItem(THEME_KEY, nextTheme);" in source


def test_frontend_maps_all_difficulties_and_alternates_sudoku_blocks():
    source = MAIN_JS.read_text()
    styles = (MAIN_JS.parent / 'styles.css').read_text()

    assert 'easy: {label: \'Easy\', clues: 45}' in source
    assert 'medium: {label: \'Medium\', clues: 35}' in source
    assert 'hard: {label: \'Hard\', clues: 30}' in source
    assert 'block-light' in source
    assert 'block-dark' in source
    assert '.sudoku-cell.block-light' in styles
    assert '.sudoku-cell.block-dark' in styles