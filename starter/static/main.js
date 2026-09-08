// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const LEADERBOARD_KEY = 'sudokuLeaderboard';
const THEME_KEY = 'sudokuTheme';
const MAX_SCORES = 10;
const DIFFICULTIES = {
  easy: {label: 'Easy', clues: 45},
  medium: {label: 'Medium', clues: 35},
  hard: {label: 'Hard', clues: 30}
};
let puzzle = [];
let timerId = null;
let gameStartedAt = null;
let gameCompleted = false;

function applyTheme(theme) {
  const selectedTheme = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = selectedTheme;
  const toggle = document.getElementById('theme-toggle');
  toggle.innerText = selectedTheme === 'dark' ? 'Light Mode' : 'Dark Mode';
  toggle.setAttribute('aria-pressed', selectedTheme === 'dark' ? 'true' : 'false');
}

function loadTheme() {
  try {
    return localStorage.getItem(THEME_KEY) === 'dark' ? 'dark' : 'light';
  } catch (error) {
    return 'light';
  }
}

function toggleTheme() {
  const nextTheme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  try {
    localStorage.setItem(THEME_KEY, nextTheme);
  } catch (error) {
    // The theme still applies when storage is unavailable.
  }
  applyTheme(nextTheme);
}

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

function updateTimer() {
  const elapsed = Math.floor((Date.now() - gameStartedAt) / 1000);
  document.getElementById('timer').innerText = formatTime(elapsed);
}

function startTimer() {
  if (timerId !== null) clearInterval(timerId);
  gameStartedAt = Date.now();
  updateTimer();
  timerId = setInterval(updateTimer, 1000);
}

function stopTimer() {
  if (timerId !== null) {
    clearInterval(timerId);
    timerId = null;
  }
}

function loadScores() {
  try {
    const stored = JSON.parse(localStorage.getItem(LEADERBOARD_KEY) || '[]');
    if (!Array.isArray(stored)) return [];
    return stored.filter((score) => (
      score && typeof score.name === 'string' && score.name.trim() &&
      Number.isFinite(score.time) && score.time >= 0 &&
      typeof score.difficulty === 'string'
    )).sort((a, b) => a.time - b.time).slice(0, MAX_SCORES);
  } catch (error) {
    return [];
  }
}

function saveScores(scores) {
  try {
    localStorage.setItem(LEADERBOARD_KEY, JSON.stringify(scores));
  } catch (error) {
    // Storage may be unavailable; the game can still be played.
  }
}

function renderLeaderboard() {
  const body = document.getElementById('leaderboard-body');
  body.innerHTML = '';
  loadScores().forEach((score, index) => {
    const row = document.createElement('tr');
    [index + 1, score.name, formatTime(score.time), score.difficulty].forEach((value) => {
      const cell = document.createElement('td');
      cell.innerText = value;
      row.appendChild(cell);
    });
    body.appendChild(row);
  });
}

function recordScore(name, time, difficulty) {
  const scores = loadScores();
  scores.push({name: name.trim(), time, difficulty});
  scores.sort((a, b) => a.time - b.time);
  saveScores(scores.slice(0, MAX_SCORES));
  renderLeaderboard();
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const settings = DIFFICULTIES[difficulty] || DIFFICULTIES.medium;
  const res = await fetch(`/new?clues=${settings.clues}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  document.getElementById('message').innerText = '';
  gameCompleted = false;
  startTimer();
}

async function requestHint() {
  const res = await fetch('/hint');
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }
  const index = data.row * SIZE + data.col;
  const input = document.getElementById('sudoku-board').getElementsByTagName('input')[index];
  input.value = data.value;
  input.disabled = true;
  input.className = 'sudoku-cell hinted';
  msg.style.color = 'var(--message-success)';
  msg.innerText = 'One cell was filled in for you.';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--message-error)';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    if (!gameCompleted) {
      gameCompleted = true;
      stopTimer();
      const elapsed = Math.floor((Date.now() - gameStartedAt) / 1000);
      const name = window.prompt('Enter your name for the Top 10 leaderboard:');
      if (name && name.trim()) {
        const difficulty = document.getElementById('difficulty').value;
        const settings = DIFFICULTIES[difficulty] || DIFFICULTIES.medium;
        recordScore(name, elapsed, settings.label);
      }
    }
    msg.style.color = 'var(--message-success)';
    msg.innerText = 'Congratulations! You solved it!';
  } else {
    msg.style.color = 'var(--message-error)';
    msg.innerText = 'Some cells are incorrect.';
  }
}

// Wire buttons
window.addEventListener('load', () => {
  applyTheme(loadTheme());
  document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  renderLeaderboard();
  // initialize
  newGame();
});
