let oikeaNumero = Math.floor(Math.random() * 9) + 1;
let arvaukset = 0;
let valittuNumero = null;

const container = document.getElementById('nappiContainer');
for (let i = 1; i <= 9; i++) {
  const btn = document.createElement('button');
  btn.textContent = i;
  btn.className = 'numero-nappi';
  btn.onclick = () => valitseNumero(i, btn);
  container.appendChild(btn);
}

function valitseNumero(numero, btn) {
  if (btn.classList.contains('kaytetty')) return;
  valittuNumero = numero;

  document.querySelectorAll('.numero-nappi').
      forEach(b => b.classList.remove('valittu'));

  btn.classList.add('valittu');
}

function arvaa() {
  const viesti = document.getElementById('viesti');
  if (valittuNumero === null) {
    viesti.textContent = 'Valitse numero ennen arvaamista!';
    return;
  }
  arvaukset++;

  const btn = document.querySelector(
      `.numero-nappi:nth-child(${valittuNumero})`);

  if (valittuNumero < oikeaNumero) {
    viesti.textContent = `Vihje: ⬆️  Arvauksia jäljellä: ${3 - arvaukset}`;
    btn.classList.add('kaytetty');
    btn.disabled = true;
  } else if (valittuNumero > oikeaNumero) {
    viesti.textContent = `Vihje: ⬇️  Arvauksia jäljellä: ${3 - arvaukset}`;
    btn.classList.add('kaytetty');
    btn.disabled = true;
  } else if (valittuNumero === oikeaNumero) {
    sendBoolean(true)
    naytaOverlay(
        `Voitit pelin! Numero oli ${oikeaNumero}. Arvausten määrä: ${arvaukset}.`);
    btn.classList.add('valittu');
  }

  if (arvaukset === 3) {
    if (valittuNumero === oikeaNumero) {
      sendBoolean(true)
      naytaOverlay(
          `Voitit pelin! Numero oli ${oikeaNumero}. Arvausten määrä: ${arvaukset}.`);
    } else {
      sendBoolean(false)
      naytaOverlay(
          `Hävisit pelin! Numero oli ${oikeaNumero}. Arvausten määrä: ${arvaukset}.`);
    }
  }

  valittuNumero = null;
}

function naytaOverlay(teksti) {
  document.getElementById('overlayMessage').textContent = teksti;
  document.getElementById('overlay').style.display = 'flex';
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