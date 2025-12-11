const vaihtoehdot = ['kivi', 'sakset', 'paperi'];
let pelaajanPisteet = 0;
let tietokoneenPisteet = 0;
let kierros = 0;
let tietokone;
let player;

function playRound(pelaaja) {
  player = pelaaja;
  tietokone = vaihtoehdot[Math.floor(Math.random() * vaihtoehdot.length)];

  cycles = 0;
  action();
}

function voittaja() {
  if (pelaajanPisteet > tietokoneenPisteet) {
    sendBoolean(true)
    document.getElementById('hr').style.borderColor = "green"
    naytaOverlay(
        `Onneksi olkoon! Voitit pelin lukemin ${pelaajanPisteet}-${tietokoneenPisteet}!`);
  } else if (pelaajanPisteet < tietokoneenPisteet) {
    sendBoolean(false)
    document.getElementById('hr').style.borderColor = "red"
    naytaOverlay(
        `Hävisit pelin lukemin ${pelaajanPisteet}-${tietokoneenPisteet}!`);
  }
}

function naytaOverlay(teksti) {
  setTimeout(() => {
  document.getElementById('overlayMessage').textContent = teksti;
  document.getElementById('overlay').style.display = 'flex';
  }, 1000);
}

let kivi1 = document.getElementById('action1');
let kivi2 = document.getElementById('action2');
let direction = -5;
let position = 0;
let cycles = 0;

function action() {
  kivi1.src = `../static/img/kivi1.png`;
  kivi2.src = `../static/img/kivi2.png`;

  position += direction;
  if (position <= -50 || position >= 0) {
    direction *= -1;
    cycles++;
  }

  kivi1.style.top = position + 'px';
  kivi2.style.top = position + 'px';

  if (cycles < 6) {
    requestAnimationFrame(action);
  } else {
    kivi1.src = `../static/img/${player}1.png`;
    kivi2.src = `../static/img/${tietokone}2.png`;
    let tulos = '';

    if (player === tietokone) {
      tulos = 'Tasapeli!';
    } else if (
        (player === 'kivi' && tietokone === 'sakset') ||
        (player === 'sakset' && tietokone === 'paperi') ||
        (player === 'paperi' && tietokone === 'kivi')
    ) {
      tulos = 'Voitit kierroksen!';
      pelaajanPisteet++;
    } else {
      tulos = 'Hävisit kierroksen!';
      tietokoneenPisteet++;
    }

    kierros++;
    document.getElementById('result').innerText =
        `Kierros: ${kierros} ${tulos}`;
    document.getElementById('score').innerText =
        `Pisteet - Pelaaja: ${pelaajanPisteet}, Tietokone: ${tietokoneenPisteet}`;

    if (pelaajanPisteet === 3 || tietokoneenPisteet === 3) {
      voittaja();
    }
  }
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

document.addEventListener('DOMContentLoaded', async () => {
            // 📌📌📌📌 STORY box  📌📌📌📌
    await fetchStory()
    const storyContainer = document.getElementById('storyOverlay');
    const storyClose = document.getElementById('storyClose');
    storyClose.addEventListener('click', () => {
        storyContainer.className = 'story-hidden'
    })
})