const kysymykset = {
  '5 + 3': 8, '9 - 4': 5, '7 * 2': 14, '12 / 3': 4,
  '8 + 6': 14, '15 - 7': 8, '4 * 5': 20, '20 / 4': 5,
  '10 + 9': 19, '14 - 6': 8, '6 * 3': 18, '18 / 2': 9,
  '11 + 8': 19, '13 - 9': 4, '9 * 4': 36, '24 / 6': 4,
  '16 + 7': 23, '25 - 12': 13, '5 * 8': 40, '30 / 5': 6,
};

const allQuestions = Object.entries(kysymykset);
const valitut = allQuestions.sort(() => 0.5 - Math.random()).slice(0, 5);

let current = 0;
let gameOver = false;
let timeLeft = 40;
let timerId;

function showQuestion() {
  if (current < valitut.length) {
    document.getElementById('question').innerText =
        `Kysymys ${current + 1}: ${valitut[current][0]} = ?`;
    document.getElementById('answer').value = '';
    document.getElementById('result').innerText = '';
    document.getElementById('final').innerText = `Kysymyksiä jäljellä: ${5 -
    current}/5`;
  } else {
    clearInterval(timerId);
    sendBoolean(true)
    naytaOverlay(`Onneksi olkoon! Voitit pelin!`);
  }
}

function startTimer() {
  document.getElementById('timer').innerText = `Aikaa jäljellä: ${timeLeft} s`;
  timerId = setInterval(() => {
    timeLeft--;
    document.getElementById(
        'timer').innerText = `Aikaa jäljellä: ${timeLeft} s`;
    if (timeLeft <= 0) {
      clearInterval(timerId);
      sendBoolean(false)
      naytaOverlay(`Aika loppui! Hävisit pelin!`);
      gameOver = true;
    }
  }, 1000);
}

function checkAnswer() {
  if (gameOver) return;

  const userInput = parseFloat(document.getElementById('answer').value);
  const oikea = valitut[current][1];

  if (userInput === oikea) {
    document.getElementById('result').innerText = 'Oikein!';
    current++;
    setTimeout(showQuestion, 1000);
  } else {
    sendBoolean(false)
    naytaOverlay(`Väärin! Hävisit pelin!`);
    gameOver = true;
    clearInterval(timerId);
  }
}

function naytaOverlay(teksti) {
  document.getElementById('overlayMessage').textContent = teksti;
  document.getElementById('overlay').style.display = 'flex';
}

function disableButton() {
  const btn = document.getElementById('aloita');
  btn.disabled = true;
}


const menuBtn = document.getElementById('menu-btn');
const navMenu = document.getElementById('nav-menu');

menuBtn.addEventListener('click', (e) => {
  menuBtn.classList.toggle('active');
  navMenu.classList.toggle('active');
  e.stopPropagation();
});

document.addEventListener('click', (e) => {
  if (
      navMenu.classList.contains('active') &&
      !navMenu.contains(e.target) &&
      !menuBtn.contains(e.target)
  ) {
    navMenu.classList.remove('active');
    menuBtn.classList.remove('active');
  }
});