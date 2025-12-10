const suits = ['hertta', 'ruutu', 'risti', 'pata'];
const values = [
  '2',
  '3',
  '4',
  '5',
  '6',
  '7',
  '8',
  '9',
  '10',
  '11',
  '12',
  '13',
  '14'];

function createDeck() {
  let deck = [];
  for (let suit of suits) {
    for (let value of values) {
      let cardValue;
      if (['11', '12', '13'].includes(value)) cardValue = 10;
      else if (value === '14') cardValue = 11;
      else cardValue = parseInt(value);

      deck.push({
        suit: suit,
        value: cardValue,
        label: value,
        img: `../static/images/kortit/${suit}${value}.svg`,
      });
    }
  }
  deck.sort(() => Math.random() - 0.5);
  return deck;
}

function renderHand(hand, elementId) {
  const container = document.getElementById(elementId);
  container.innerHTML = '';
  hand.forEach(card => {
    const img = document.createElement('img');
    img.src = card.img;
    img.alt = `${card.suit} ${card.label}`;
    img.style.width = '80px';
    img.style.margin = '5px';
    container.appendChild(img);
  });
}

let deck = createDeck();
let playerHand = [deck.pop(), deck.pop()];
let dealerHand = [deck.pop(), deck.pop()];

let playerScore = calculateScore(playerHand);
let dealerScore = calculateScore(dealerHand);


renderHand(playerHand, 'player');
renderHand(dealerHand.slice(1), 'dealer')

function drawCard() {
  let uusiKortti = deck.pop();
  playerHand.push(uusiKortti);
  renderHand(playerHand, 'player');
  playerScore = calculateScore(playerHand);
  if (playerScore > 21) {
    sendBoolean(false)
    document.getElementById('player').style.backgroundColor = 'red';
    naytaOverlay(
        `Hävisit pelin! Korttien summa oli yli 21 (${playerScore}).`);
  }
}

function calculateScore(hand) {
  let score = 0;
  let aces = 0;

  for (let card of hand) {
    score += card.value;
    if (card.label === '14') {
      aces++;
    }
  }

  while (score > 21 && aces > 0) {
    score -= 10;
    aces--;
  }
  return score;
}

function calculateHand() {

  if (playerScore > 21) {
    sendBoolean(false)
    naytaOverlay(
        `Hävisit pelin! Sinun tulos: ${playerScore}. Jakajan tulos: ${dealerScore}`);
    return;
  }

  while (dealerScore < 17) {
    dealerHand.push(deck.pop());
    showDealer();
    dealerScore = calculateScore(dealerHand);
  }

  if (dealerScore > 21) {
    sendBoolean(true)
    document.getElementById('player').style.backgroundColor = 'green';
    naytaOverlay(
        `Voitit pelin! Sinun tulos: ${playerScore}. Jakajan tulos: ${dealerScore}`);
  } else if (playerScore > dealerScore) {
    sendBoolean(true)
    document.getElementById('player').style.backgroundColor = 'green';
    naytaOverlay(
        `Voitit pelin! Sinun tulos: ${playerScore}. Jakajan tulos: ${dealerScore}`);
  } else if (playerScore === dealerScore) {
    document.getElementById('player').style.backgroundColor = 'yellow';
    document.getElementById('dealer').style.backgroundColor = 'yellow';
    tasapeli(
        `Tasapeli. Pelaa uudelleen painamalla 'jatka'.`,
    );
  } else {
    sendBoolean(false)
    document.getElementById('dealer').style.backgroundColor = 'green';
    naytaOverlay(
        `Hävisit pelin! Sinun tulos: ${playerScore}. Jakajan tulos: ${dealerScore}`);
  }
}

function showDealer() {
  renderHand(dealerHand, 'dealer');
}

function restartGame() {
  deck = createDeck();

  document.getElementById('dealer').style.backgroundColor = 'revert';
  document.getElementById('player').style.backgroundColor = 'revert';

  playerHand = [deck.pop(), deck.pop()];
  dealerHand = [deck.pop(), deck.pop()];

  playerScore = calculateScore(playerHand);
  dealerScore = calculateScore(dealerHand);

  document.getElementById('overlay').style.display = 'none';
  document.getElementById('overlayMessage').textContent = '';

  renderHand(playerHand, 'player');
  renderHand(dealerHand.slice(1), 'dealer');
}

function naytaOverlay(teksti) {
  setTimeout(() => {
    document.getElementById('overlayMessage').textContent = teksti;
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('overlayLink').
        removeEventListener('click', restartHandler);
  }, 2000);
}

function tasapeli(teksti) {
  setTimeout(() => {
    document.getElementById('overlayMessage').textContent = teksti;
    document.getElementById('overlay').style.display = 'flex';
    document.getElementById('overlayLink').
        addEventListener('click', restartHandler);
  }, 2000);
}

function restartHandler(event) {
  event.preventDefault();
  restartGame();
}

function ohjeet() {
  document.getElementById('ohjeOverlay').style.display = 'flex';
  document.getElementById('ohjeButton').addEventListener('click', function(event) {
    document.getElementById('ohjeOverlay').style.display = 'none'
  })
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