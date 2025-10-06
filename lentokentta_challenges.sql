-- SQL seed file: Lentokenttäpelit – maat ja tarinat
-- Taulu: stories
-- Kentät: id, country, story

DROP TABLE IF EXISTS stories;

CREATE TABLE stories (
  id INTEGER PRIMARY KEY,
  country TEXT NOT NULL,
  story TEXT NOT NULL
);

INSERT INTO stories VALUES(1,'Suomi','Olet saapunut Suomeen! Lentokentällä vastaasi tulee hätääntyneen oloinen henkilö. Hän on unohtanut matkalaukkunsa koodin viimeisen numeron. Arvaamalla oikean luvun 1-9 välillä, saat palkinnoksi Heva-haalariherkin.');
INSERT INTO stories VALUES(2,'Ruotsi','Välkommen till Sverige! Etsiessäsi kuumeisesti seuraavan lennon porttia, näet lentokentän lattialla komeilemassa haalarimerkin. Kiiruahtaessasi sitä kohden, huomaat, että sinulla on kilpailija. Molempien tarttuessa haalarimerkkiin päätätte ratkaista taiston kivi-sakset-paperi pelillä. Voittaja saa haalarimerkin.');
INSERT INTO stories VALUES(3,'Tanska','Odottaessasi seuraavaa lentoa vieressä istuva lapsi pyytää sinulta apua kotitehtävien ratkaisemiseen. Hän tarjoaa palkinnoksi haalarimerkkiä, mikäli saat kaikki vastaukset oikein.');
INSERT INTO stories VALUES(4,'Viro','Odotellessasi seuraavaa siirtymää, päätät käydä lentokentän kasinolla. Kasinolla on Blackjack peli, jossa palkintona on haalarimerkki.');
INSERT INTO stories VALUES(5,'Alankomaat','Amsterdam tunnetaan kanaaleistaan, ja haluat ostaa lentokentän matkamuistomyymälästä siihen liittyvän pienoismallin. Ostoksen yhteydessä osallistut myymälän wordle-peliin, josta voit voittaa kaupan päälle haalarimerkin.');
INSERT INTO stories VALUES(6,'Andorra','Nauttiessasi Andorran vuoristoilmasta, huomaat lentokentän pääsisäänkäynnin yhteydessä kojun. Kojussa järjestetään Hirsipuu-peli, jonka voittaja saa haalarimerkin. Päätät tarttua tilaisuuteen ja osallistut peliin.');
INSERT INTO stories VALUES(7,'Turkki','Vessakäyntisi jälkeen suuntaat hakemaan laukkusi lokerikosta. Lokerikon vieressä seisoo hermostuneen näköinen henkilö. Hän on unohtanut mihin yhdeksästä lokerosta hän on laittanut matkatavaransa. Jos onnistut arvaamaan oikean lokeron, saat palkinnoksi haalarimerkin.');
INSERT INTO stories VALUES(8,'Kreikka','Päätät ostaa matkamuistoksi kreikkalaisen viinapullon lentokentältä. Tarttuessasi pulloon, huomaat ettet ole ainoa pullosta kiinnostunut. Päätätte ratkaista kiistan kivi-sakset-paperi menetelmällä. Voittaja saisi pullon, jonka ohessa on haalarimerkki.');
INSERT INTO stories VALUES(9,'Azerbaidžan','Bakun lentokentän odotusaulassa koululainen levittää vihkonsa viereiselle penkille. Hän kysyy, osaisitko auttaa muutamassa matikkatehtävässä. Jos ratkaiset ne oikein, hän lupaa antaa haalarimerkin.');
INSERT INTO stories VALUES(10,'Serbia','Belgradin porttialueella opiskelijakerho on pystyttänyt pienen korttipöydän viihdyttääkseen myöhästyneitä matkustajia. Päätät osallistua toiveissa voittaa luvattu haalarimerkki.');
INSERT INTO stories VALUES(11,'Saksa','Berliinin lentoaseman kirjakaupan seinällä vilkkuu päivän sana. Myyjä kertoo, että jos ratkaiset sen ennen kuin koneesi lähtee, saat haalarimerkin.');
INSERT INTO stories VALUES(12,'Slovakia','Bratislavan turvatarkastuksen jälkeen on pieni opiskelijakoju, jossa voi pelata Hirsipuuta. Jos arvaat sanan oikein ennen kuulutusta saat haalarimerkin.');
INSERT INTO stories VALUES(13,'Sveitsi','Bernin lentokentän säilytyslokeroiden luona työntekijä kuiskaa: “Yhteen niistä olen piilottanut haalarimerkin.” Jos arvaat oikean lokeron, haalarimerkki on sinun.');
INSERT INTO stories VALUES(14,'Belgia','Brysselin portilla on pieni suklaapuoti, jossa on myynnissä limited edition suklaarasia. Sinä ja toinen asiakas haluatte tämän kyseisen tuotteen sen herkullisen suklaan ja haalarimerkin vuoksi. Myyjä ehdottaa kivi-sakset-paperi -ratkaisua, jolloin kiista saadaan ratkaistua reilusti.');
INSERT INTO stories VALUES(15,'Unkari','Budapestin terminaalin kahvilassa opiskelijajärjestö myy kahvia ja järjestää matikkavisan matkustajille. Jos lasket kaikki oikein, saat haalarimerkin.');
INSERT INTO stories VALUES(16,'Romania','Lentoyhtiön työntekijä odottaa koneen lähtöaikaa ja ehdottaa sinulle pientä peliä. “Minulla on kortit ja haalarimerkki. Katsotaan, kumpi saa 21 ensin.” Matkustajat alkavat seurata vierestä tätä mielenkiintoista spektaakkelia.');
INSERT INTO stories VALUES(17,'Moldova','Matkamuistomyymälässä päivän ostokseen sisältyy Wordle-peli. Arvaa oikein ennen kuin kuittitulostin lakkaa surisemasta, niin saat haalarimerkin kaupan päälle.');
INSERT INTO stories VALUES(18,'Irlanti','Dublinin lentoaseman kahvilan ilmoitustaululla on Hirsipuu-peli liitutaululle kirjoitettuna. Barista lupaa haalarimerkin jokaiselle asiakkaalle, joka onnistuu voittamaan.');
INSERT INTO stories VALUES(19,'Armenia','Jerevanin lähtöporttien ilmoitustaululla lukee “Mikä portti avautuu ensimmäisenä?”. Jos arvaat oikean numeron, saat palkinnoksi haalarimerkin.');
INSERT INTO stories VALUES(20,'Ukraina','Kiovan lentokentän kahvilan vitriinissä on enää yksi erikoiskahvi jäljellä. Sinä ja toinen asiakas ojennatte kätenne yhtä aikaa sitä kohden. Myyjä hymyilee ja ehdottaa kivi-sakset-paperi -ratkaisua. Voittaja saa sekä kahvin, että haalarimerkin.');
INSERT INTO stories VALUES(21,'Portugali','Lissabonin terminaalissa on “päivän haaste” -koju, jossa matkustajia pyydetään ratkaisemaan nopeita laskuja. Jos onnistut ratkaisemaan kaikki oikein, opiskelijat palkitsevat sinut haalarimerkillä.');
INSERT INTO stories VALUES(22,'Slovenia','Kuulutus kertoo tunnin viivästyksestä. Lentokenttä järjestää spontaanisti “viihdehetken” viereisellä tiskillä. “Blackjack-turnaus, voittajalle haalarimerkki!” Kaikki huokaavat helpotuksesta — jotain tekemistä odotteluun.');
INSERT INTO stories VALUES(23,'Iso-Britannia','Lontoon Heathrow’n kirjakaupassa päivän Wordle on kirjoitettu infonäytölle. “Ratkaise ennen boardingia ja saat haalarimerkin”, myyjä sanoo.');
INSERT INTO stories VALUES(24,'Luxemburg','Luxemburgin lentoaseman kahvilan pöydällä on tabletti, jossa pyörii Hirsipuu. Jos arvaat oikean sanan ennen kuulutusta, saat haalarimerkin.');
INSERT INTO stories VALUES(25,'Espanja','Madridin matkatavarakarusellin yläpuolella on numeroita. Jos onnistut arvaamaan minkä numeron kohdalla matkatavarasi pysähtyy, voitat haalarimerkin.');
INSERT INTO stories VALUES(26,'Valko-Venäjä','Minskin porttialueella opiskelijajärjestö pitää kojua. Jos voitat kojun pitäjän kivi-sakset-paperi-pelissä, voitat haalarimerkin.');
INSERT INTO stories VALUES(27,'Venäjä','Moskovan lentoaseman kahvilan tiskillä on kyltti: “Ratkaise matikkapulmat ja saat ilmaisen kahvin ja haalarimerkin.');
INSERT INTO stories VALUES(28,'Kypros','Nikosian lentokentän aurinkoiselle terassille on pystytetty Blackjack-pöytä. Voitosta jää muistoksi haalarimerkki.');
INSERT INTO stories VALUES(29,'Norja','Oslon lentoaseman lahjapuodin myyjä ilmoittaa, että oikean sanan arvaaja saa ostokselleen alennuksen, sekä haalarimerkin.');
INSERT INTO stories VALUES(30,'Tšekki','Prahan porttialueella matkustajat odottavat lentoaan pelaten Hirsipuuta digitaalisella taululla. Oikea sana paljastaa koodin, jolla voi lunastaa haalarimerkin infopisteeltä.');
INSERT INTO stories VALUES(31,'Ranska','Pariisin Charles de Gaullen säilytystiskillä työntekijä järjestää pienen pelin: “Valitse lokero – yksi niistä kätkee pienen yllätyksen.” Valitse oikein ja saat haalarimerkin.');
INSERT INTO stories VALUES(32,'Montenegro','Podgorican kentällä pubin tiskillä on kyltti: “Haasta baarimikko kivi–sakset–paperiin. Jos voitat, onnesi tuo haalarimerkin.”.');
INSERT INTO stories VALUES(33,'Kosovo','Prištinan terminaalin kahvila on täynnä opiskelijoita, jotka jakavat lentokortteja – mutta niissä on yhtälöitä. Ratkaise kaikki korttisi tehtävät oikein ja saat haalarimerkin palkinnoksi.');
INSERT INTO stories VALUES(34,'Islanti','Reykjavikin lentoaseman loungessa väsyneen näköiset matkaajat ovat rakentaneet minikasinon. Jos voitat jakajan, saat haalarimerkin.');
INSERT INTO stories VALUES(35,'Latvia','Riikan infonäytöllä pyörii sanapeli, johon matkustajat voivat osallistua puhelimillaan. Oikein arvanneet saavat haalarimerkin.');
INSERT INTO stories VALUES(36,'Italia','Rooman lentokentän kahvilassa Hirsipuu pyörii pöytään upotetulla näytöllä. Arvaa sana niin saat kassalta haalarimerkin.');
INSERT INTO stories VALUES(37,'Bosnia ja Hertsegovina','Sarajevon check-in -pisteellä virkailija vilkaisee näyttöä ja sanoo: “Jos arvaat, mikä numero toistuu lentosi varauskoodissa, annan sinulle haalarimerkin.”');
INSERT INTO stories VALUES(38,'Pohjois-Makedonia','Kun annat passin tiskillä, virkailija kuiskaa: “Meillä on tänään peli. Jos voitat minut kivi–sakset–paperissa, saat haalarimerkin, jonka vain harvat saavat.”');
INSERT INTO stories VALUES(39,'Bulgaria','Sofian lentoaseman kahviossa opiskelijaryhmä haastaa matkustajia “päässälaskumaratoniin”. Jos suoritat kierroksen ennen boardingia, he palkitsevat sinut haalarimerkillä. Mutta varo! Yksikin väärin ja et saa mitään.');
INSERT INTO stories VALUES(40,'Georgia','Lentokentän pienellä pelialueella on automaatti, joka mainostaa: “Kokeile onneasi – voita jakaja ja saat haalarimerkin!” Automaatti piippaa, kortit vilahtavat ruudulla, ja jännitys kasvaa boarding-kuulutuksen yli.');
INSERT INTO stories VALUES(41,'Albania','Rahanvaihtotiskillä on kyltti: “Arvaa päivän sana, niin valuuttakurssien lisäksi haalarimerkkien määrä vaihtuu.”');
INSERT INTO stories VALUES(42,'Malta','Vallettan lentokentän rantateemaisessa kahvilassa pelataan Hirsipuuta. Kun arvaat sanan, tarjoilija antaa sinulle haalarimerkin.');
INSERT INTO stories VALUES(43,'Puola','Portin työntekijä järjestää ajankuluksi pienen kilpailun: “Arvatkaa, mikä seuraavista porteista avautuu ensimmäisenä!” Voittajalle annetaan pieni muistaminen – haalarimerkki.');
INSERT INTO stories VALUES(44,'Liettua','Vilnan odotusaulassa matkustajat kilpailevat kivi-sakset-paperilla viihteeksi ennen lentoa. Liityt mukaan, voitat kierroksen – ja saat haalarimerkin.');
INSERT INTO stories VALUES(45,'Itävalta','Wienin lentoaseman kahvilassa tarjoilija testaa asiakkaiden laskupäätä ennen laskun maksua. Jos ratkaiset kaikki laskutoimituksen oikein, saat kaupan päälle haalarimerkin.');
INSERT INTO stories VALUES(46,'Kroatia','Lentokentän yökahvilassa barista sekoittaa kortteja tylsistyneenä. “Tämä paikka nukkuu, mutta peli ei. Pelaatko kierroksen?” Hän napauttaa pöytää. “Blackjack – ja jos voitat, ansaitset haalarimerkin.”');
