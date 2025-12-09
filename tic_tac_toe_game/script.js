const cells = document.querySelectorAll('.cell');
const message = document.getElementById('message');
const restartButton = document.getElementById('restartButton');

let board = ['', '', '', '', '', '', '', '', ''];
let currentPlayer = 'X';
let isGameActive = true;

const winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 4, 6],
    [0, 4, 8],
    [2, 4, 6]
];

function handleCellClick(e) {
    const clickedCell = e.target;
    const clickedCellIndex = parseInt(clickedCell.dataset.cellIndex);

    if (board[clickedCellIndex] !== '' || !isGameActive) {
        return;
    }

    board[clickedCellIndex] = currentPlayer;
    clickedCell.textContent = currentPlayer;
    clickedCell.classList.add(currentPlayer.toLowerCase()); // Add class for animation

    checkResult();
}

function showMessage(msg) {
    message.textContent = msg;
    message.classList.add('message-fade-in'); // Add animation class
    setTimeout(() => {
        message.classList.remove('message-fade-in');
    }, 500); // Remove after animation duration
}

function checkResult() {
    let roundWon = false;
    for (let i = 0; i < winningConditions.length; i++) {
        const winCondition = winningConditions[i];
        const a = board[winCondition[0]];
        const b = board[winCondition[1]];
        const c = board[winCondition[2]];

        if (a === '' || b === '' || c === '') {
            continue;
        }
        if (a === b && b === c) {
            roundWon = true;
            break;
        }
    }

    if (roundWon) {
        showMessage(`Player ${currentPlayer} has won!`);
        isGameActive = false;
        return;
    }

    const roundDraw = !board.includes('');
    if (roundDraw) {
        showMessage('It\'s a draw!');
        isGameActive = false;
        return;
    }

    changePlayer();
}

function changePlayer() {
    currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
    showMessage(`It's ${currentPlayer}'s turn`);
}

function restartGame() {
    isGameActive = false; // Temporarily deactivate to prevent clicks during reset
    showMessage('Restarting...');

    setTimeout(() => {
        board = ['', '', '', '', '', '', '', '', ''];
        currentPlayer = 'X';
        isGameActive = true;

        cells.forEach(cell => {
            cell.textContent = '';
            cell.classList.remove('x', 'o'); // Remove classes to reset animations
        });

        showMessage(`It's ${currentPlayer}'s turn`);
    }, 700); // Give time for message animation or a brief visual reset

}

cells.forEach(cell => cell.addEventListener('click', handleCellClick));
restartButton.addEventListener('click', restartGame);

// Initial message
showMessage(`It's ${currentPlayer}'s turn`);
