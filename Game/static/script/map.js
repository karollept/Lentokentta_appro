const countryAirports = {
  FI: {name: 'Helsinki-Vantaa', logo: '../static/images/haalarimerkit/Hevan.png', connections: ['Tukholma - 202€','Kööpenhamina - 279€','Tallinna - 224€']},
  SE: {name: 'Stockholm Arlanda', logo: '../static/images/haalarimerkit/Tuk.png', connections: ['Helsinki-Vantaa - 216€','Oslo Gardermoen - 189€','Berlin - 255€']},
  DK: {name: 'Kööpenhamina', logo: '../static/images/haalarimerkit/Kopa.png', connections: ['Helsinki-Vantaa - 252€','Keflavík Interna. - 285€','Warsaw Chopin - 276€']},
  EE: {name: 'Tallinna', logo: '../static/images/haalarimerkit/Tali.png', connections: ['Helsinki-Vantaa - 216€','Riga International - 222€','Vilnius Airport - 251€']},
  NL: {name: 'Schiphol', logo: '../static/images/haalarimerkit/Schii.png', connections: ['Berlin - 264€','Brussels Airport - 261€','Vienna Interna. - 278€']},
  AD: {name: 'Andorra–La Seu d\'Urgell', logo: '../static/images/haalarimerkit/Andi.png', connections: ['Charles de Gaulle - 279€','Adolfo Suárez - 230€','Heathrow Airport - 296€']},
  TR: {name: 'Ankara Esenboga', logo: '../static/images/haalarimerkit/Anka.png', connections: ['Larnaca Interna. - 255€','Tbilisi International - 286€','Sheremetyevo - 296€']},
  GR: {name: 'Eleftherios Venizelos', logo: '../static/images/haalarimerkit/Efe.png', connections: ['Larnaca Interna. - 259€','Tirana Interna. - 266€','Skopje Interna. - 271€']},
  AZ: {name: 'Baku International Airport', logo: '../static/images/haalarimerkit/Bakuza.png', connections: ['Tbilisi International - 299€','Sheremetyevo - 284€','Zvartnots Interna. - 274€']},
  RS: {name: 'Belgrade Nikola Tesla Airport', logo: '../static/images/haalarimerkit/Tesli.png', connections: ['Pristina Interna. - 206€','Sarajevo Interna. - 197€','Boryspil Interna. - 268€']},
  DE: {name: 'Berlin Brandenburg Airport', logo: '../static/images/haalarimerkit/Berli.png', connections: ['Tukholma - 254€','Schiphol - 270€','Brussels Airport - 259€']},
  SK: {name: 'M. R. Stefanik Airport', logo: '../static/images/haalarimerkit/Stefi.png', connections: ['Václav Havel - 267€','Budapest Ferenc - 202€','Chișinău Interna. - 264€']},
  CH: {name: 'Bern Airport', logo: '../static/images/haalarimerkit/Berni.png', connections: ['Vienna Interna. - 274€','Luxembourg - 192€','Larnaca Interna. - 305€']},
  BE: {name: 'Brussels Airport', logo: '../static/images/haalarimerkit/Brus.png', connections: ['Schiphol - 286€','Berlin - 268€','Franjo Tuđman - 291€']},
  HU: {name: 'Budapest Ferenc Liszt Intl Airport', logo: '../static/images/haalarimerkit/Liszi.png', connections: ['M. R. Stefanik - 216€','Sofia Airport - 255€','Henri Coandă - 252€']},
  RO: {name: 'Henri Coandă International Airport', logo: '../static/images/haalarimerkit/Coanda.png', connections: ['Minsk National - 318€','Boryspil Interna. - 279€','Budapest Ferenc - 274€']},
  MD: {name: 'Chișinău International Airport', logo: '../static/images/haalarimerkit/Chisi.png', connections: ['Boryspil Interna. - 198€','Adolfo Suárez - 293€','M. R. Stefanik - 271€']},
  IE: {name: 'Dublin Airport', logo: '../static/images/haalarimerkit/Dubli.png', connections: ['Keflavík Interna. - 272€','Heathrow Airport - 206€','Humberto Delgado - 294€']},
  AM: {name: 'Zvartnots International Airport', logo: '../static/images/haalarimerkit/Zvarti.png', connections: ['Baku International - 253€','Tbilisi International - 270€','Luxembourg - 287€']},
  UA: {name: 'Boryspil International Airport', logo: '../static/images/haalarimerkit/Boris.png', connections: ['Chișinău Interna. - 210€','Henri Coandă - 251€','Belgrade Nikola - 277€']},
  PT: {name: 'Humberto Delgado Airport', logo: '../static/images/haalarimerkit/Humb.png', connections: ['Malta International - 298€','Adolfo Suárez - 270€','Dublin Airport - 299€']},
  SI: {name: 'Ljubljana Jože Pučnik Airport', logo: '../static/images/haalarimerkit/Ljubl.png', connections: ['Franjo Tuđman - 211€','Leonardo da Vinci - 213€','Riga International - 296€']},
  GB: {name: 'Heathrow Airport', logo: '../static/images/haalarimerkit/Heath.png', connections: ['Andorra–La - 319€','Dublin Airport - 227€','Václav Havel - 259€']},
  LU: {name: 'Luxembourg Airport', logo: '../static/images/haalarimerkit/Luxi.png', connections: ['Charles de Gaulle - 236€','Bern Airport - 234€','Zvartnots Interna. - 259€']},
  ES: {name: 'Adolfo Suárez Madrid–Barajas Airport', logo: '../static/images/haalarimerkit/Madria.png', connections: ['Andorra-La - 216€','Humberto Delgado - 278€','Chișinău Interna. - 293€']},
  BY: {name: 'Minsk National Airport', logo: '../static/images/haalarimerkit/Minski.png', connections: ['Riga International - 192€','Sheremetyevo - 251€','Henri Coandă - 300€']},
  RU: {name: 'Sheremetyevo International Airport', logo: '../static/images/haalarimerkit/Sheri.png', connections: ['Minsk National - 262€','Baku International - 277€','Ankara - 298€']},
  CY: {name: 'Larnaca International Airport', logo: '../static/images/haalarimerkit/Larna.png', connections: ['Ankara - 275€','Eleftherios - 261€','Bern Airport - 298€']},
  NO: {name: 'Oslo Gardermoen Airport', logo: '../static/images/haalarimerkit/Oslis.png', connections: ['Tukholma - 213€','Keflavík Interna. - 277€','Vilnius Airport - 294€']},
  CZ: {name: 'Václav Havel Airport Prague', logo: '../static/images/haalarimerkit/Havel.png', connections: ['M. R. Stefanik - 282€','Warsaw Chopin - 292€','Heathrow Airport - 286€']},
  FR: {name: 'Charles de Gaulle Airport', logo: '../static/images/haalarimerkit/DeGau.png', connections: ['Andorra-La - 274€','Luxemburg - 184€','Malta International - 320€']},
  ME: {name: 'Podgorica Airport', logo: '../static/images/haalarimerkit/Podgo.png', connections: ['Pristina Interna. - 226€','Sofia Airport - 192€','Sarajevo Interna. - 180€']},
  XK: {name: 'Pristina International Airport', logo: '../static/images/haalarimerkit/Pristi.png', connections: ['Tirana Interna. - 229€','Podgorica Airport - 222€','Belgrade Nikola - 224€']},
  IS: {name: 'Keflavík International Airport', logo: '../static/images/haalarimerkit/Kefi.png', connections: ['Kööpenhamina - 281€','Dublin Airport - 286€','Oslo Gardermoen - 266€']},
  LV: {name: 'Riga International Airport', logo: '../static/images/haalarimerkit/Rigi.png', connections: ['Tallinna - 226€','Minsk National - 184€','Ljubljana Jože - 301€']},
  IT: {name: 'Leonardo da Vinci–Fiumicino Airport', logo: '../static/images/haalarimerkit/Vinci.png', connections: ['Vienna Interna. - 253€','Tirana Interna. - 276€','Ljubljana Jože - 217€']},
  BA: {name: 'Sarajevo International Airport', logo: '../static/images/haalarimerkit/Sare.png', connections: ['Belgrade Nikola - 200€','Skopje Interna. - 268€','Podgorica Airport - 184€']},
  MK: {name: 'Skopje International Airport', logo: '../static/images/haalarimerkit/Skopi.png', connections: ['Eleftherios - 199€','Sarajevo Interna. - 200€','Sofia Airport - 224€']},
  BG: {name: 'Sofia Airport', logo: '../static/images/haalarimerkit/Sofi.png', connections: ['Podgorica Airport - 218€','Budapest Ferenc - 277€','Skopje Interna. - 261€']},
  GE: {name: 'Tbilisi International Airport', logo: '../static/images/haalarimerkit/Tibi.png', connections: ['Baku International - 265€','Zvartnots Interna. - 282€','Ankara - 255€']},
  AL: {name: 'Tirana International Airport (Nënë Tereza)', logo: '../static/images/haalarimerkit/Tiran.png', connections: ['Eleftherios - 264€','Leonardo da Vinci - 254€','Pristina Interna. - 223€']},
  MT: {name: 'Malta International Airport', logo: '../static/images/haalarimerkit/Malti.png', connections: ['Humberto Delgado - 313€','Franjo Tuđman - 307€','Charles de Gaulle - 313€']},
  PL: {name: 'Warsaw Chopin Airport', logo: '../static/images/haalarimerkit/Warcho.png', connections: ['Kööpenhamina - 265€','Vilnius Airport - 211€','Václav Havel - 272€']},
  LT: {name: 'Vilnius Airport', logo: '../static/images/haalarimerkit/Vilu.png', connections: ['Warsaw Chopin - 206€','Tallinna - 251€','Oslo Gardermoen - 293€']},
  AT: {name: 'Vienna International Airport', logo: '../static/images/haalarimerkit/Vieni.png', connections: ['Bern Airport - 251€','Leonardo da Vinci - 269€','Schipholin - 272€']},
  HR: {name: 'Franjo Tuđman Airport', logo: '../static/images/haalarimerkit/Tuda.png', connections: ['Brussels Airport - 299€','Ljubljana Jože - 211€','Malta International - 317€']}  
};

function updateInfo(airport) {
  const infoDiv = document.getElementById('info');
  document.getElementById('airport-name').textContent = airport.name;
  document.getElementById('airport-connections').innerHTML = airport.connections.join('<br>');
  document.getElementById('airport-logo').src = airport.logo;
  infoDiv.style.display = 'block';
}

const paths = document.querySelectorAll('#europe-map path');

paths.forEach(path => {
  path.addEventListener('click', () => {
    paths.forEach(p => p.classList.remove('selected-country'));

    path.classList.add('selected-country');

    const airport = countryAirports[path.id];
    if (airport) updateInfo(airport);
  });
});
