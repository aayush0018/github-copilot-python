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