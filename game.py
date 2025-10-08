import mysql.connector
import random

yhteys = mysql.connector.connect(
    host="localhost",
    user="user",
    password = "password",
    autocommit = True,
    db = "lk_approt",
    port = 3306
)
cursor = yhteys.cursor()

#pelaajan valinta
def choose_player(location, budget):
    c= yhteys.cursor()

    nimi = input("Anna pelinimesi: ").strip()  #poistaa välilyönnit alusta ja lopusta
    if nimi == "":
        print("Tyhjää merkkijona ei hyväksytä.")
        return None

    vapaa = is_name_taken(nimi)

    if vapaa == None:
        c.execute("INSERT INTO player (screen_name, location, budget) VALUES (%s, %s, %s)",
                    (nimi, location, budget))
        c.close()
        return nimi

    else:
        print("Pelaaja nimi varattu, valitse toinen")
        return None


def is_name_taken(nimi):
    c = yhteys.cursor()
    c.execute("SELECT screen_name FROM player WHERE screen_name = (%s)",
               (nimi,))
    tulos = c.fetchall()

    c.close()

    return tulos[0] if len(tulos) > 0 else None


def flight_paths(location):
  c = yhteys.cursor()

  sql= ("SELECT name, connection.price FROM airport "
        "INNER JOIN connection on airport.ident=connection.ident2 "
        "WHERE ident1 = %s")
  c.execute(sql, (location,))

  tulos = c.fetchall()
  c.close()

  return tulos


def flight_choise(connections, budget):
    print(f"Budjettisi = {budget}€\n"
        "Valitse minne kentälle haluat lentää:")

    for i in range(len(connections)):
        print(f"{i+1}. {connections[i][0]} - {connections[i][1]}€")

    while True:
        choise = input("")
        if choise.isdigit():
            int_choise = int(choise)
            if int_choise <= len(connections):
                return connections[int(choise) - 1]

        print(f"Virhe! syötä kenttään vain kokonais luku väliltä 1-{len(connections)}.")


def update_player(tuple, player, budget):
    c = yhteys.cursor()

    new_budget= budget-tuple[1]
    airport = tuple[0]
    sql=("UPDATE player SET location = ("
         "SELECT ident FROM airport WHERE airport.name = %s), "
         "budget = %s "
         "WHERE screen_name = %s")

    c.execute(sql, (airport, new_budget, player))

    c.execute("SELECT ident FROM airport WHERE name = %s", (airport,))
    new_location = c.fetchone()[0]
    c.close()

    return new_budget, new_location

def play_game():
    cursor = yhteys.cursor()

    sql = (
        "SELECT airport.ident, minigame.name FROM airport "
        "JOIN minigame ON airport.minigame_id = minigame.id "
        "JOIN player ON airport.ident = player.location "
        "WHERE player.id = 6")

    cursor.execute(sql)
    tulos = cursor.fetchone()

    if tulos:
        location = tulos[0]
        minipelin_nimi = tulos[1]
        print(f"Pelaaja on kentällä {location}, minipeli on: {minipelin_nimi}")

        # Käynnistä minipeli nimen perusteella
        if minipelin_nimi == "Kivi_sakset_paperi":
            kivi_sakset_paperi()
        elif minipelin_nimi == "Wordle":
            wordle()
        elif minipelin_nimi == "Hirsipuu":
            hirsipuu()
        elif minipelin_nimi == "Matikkavisa":
            matikkavisa()
        elif minipelin_nimi == "Blackjack":
            blackjack()
        elif minipelin_nimi == "Numeron arvaus":
            numeron_arvauspeli()
        else:
            print("Tuntematon minipeli tietokannassa.")
    else:
        print("Kentälle ei ole liitetty minipeliä.")

def kivi_sakset_paperi():
    print("Tervetuloa Kivi–Sakset–Paperi -peliin! Pelataan 3 kierrosta.")
    vaihtoehdot = ["kivi", "sakset", "paperi"]
    pelaajan_pisteet = 0
    tietokoneen_pisteet = 0

    for kierros in range(1, 4):
        print(f"\nKierros {kierros}:")
        while True:
            pelaaja = input("Valitse kivi, sakset tai paperi: ").lower()
            if pelaaja not in vaihtoehdot:
                print("Virheellinen valinta. Yritä uudelleen.")
                continue
            break

        tietokone = random.choice(vaihtoehdot)
        print(f"Tietokone valitsi: {tietokone}")

        if pelaaja == tietokone:
            print("Tasapeli!")
        elif (pelaaja == "kivi" and tietokone == "sakset") or \
                (pelaaja == "sakset" and tietokone == "paperi") or \
                (pelaaja == "paperi" and tietokone == "kivi"):
            print("Voitit kierroksen!")
            pelaajan_pisteet += 1
        else:
            print("Hävisit kierroksen!")
            tietokoneen_pisteet += 1

    print("\nPeli päättyi!")
    print(f"Pisteet - Pelaaja: {pelaajan_pisteet}, Tietokone: {tietokoneen_pisteet}")

    if pelaajan_pisteet > tietokoneen_pisteet:
        voitto = True
        print("Onneksi olkoon! Voitit pelin!")
    elif pelaajan_pisteet < tietokoneen_pisteet:
        print("Hävisit pelin!")
        voitto = False
    else:
        print("Peli päättyi tasapeliin!")
        voitto = False
    return voitto

def numeron_arvauspeli():
    print("Tervetuloa numeron arvauspeliin!")
    print("Ajattelen numeroa 1 ja 9 välillä...")

    oikea_numero = random.randint(1, 9)
    arvaukset = 0

    while True:
        try:
            arvaus = int(input("Arvaa numero: "))
            arvaukset += 1

            if arvaus < oikea_numero:
                print("Liian pieni! Yritä uudelleen.")
            elif arvaus > oikea_numero:
                print("Liian suuri! Yritä uudelleen.")
            else:
                print(f"Onneksi olkoon! Arvasit oikein numeron {oikea_numero} {arvaukset} yrityksellä.")
                voitto = True
                break
        except ValueError:
            print("Ole hyvä ja syötä kokonaisluku.")
    return voitto

def vastaus_wordle_def():
    wordle_id = [random.randint(1,1426)]

    cursor.execute("SELECT sana from wordle WHERE id = %s", wordle_id)
    rows = cursor.fetchall()

    for (i,) in rows:
        vastaus = list(i)  #muutetaan vastaus listaksi jossa jokainen kirjain on yksi arvo

    return vastaus


def checker_wordle(vastaus, arvaus_list):
    checker = []

    for i in range(5):
        if arvaus_list[i] == vastaus[i]:
            checker.append("green")
        elif arvaus_list[i] in vastaus:
            checker.append("yellow")             # laitetaan wordle_checker listaan jokaisen kirjaimen kohdalle oikea arvo (oikea paikka, oikea kirjain, väärin)
        else:
            checker.append("reset")
    return checker


def wordle_arvaus_def(arvaus):
    arvaus_list = []

    for kirjain in arvaus:
        arvaus_list.append(kirjain)  # muunnetaan arvaus listaksi, jossa jokainen kirjain on listan arvo

    return arvaus_list

def wordle_5letters():
    loop_wordle_5letters = True
    while loop_wordle_5letters == True:
        arvaus = input("")
        if len(arvaus) == 5 and type(
                arvaus) == str:  # Tarkistetaan, että käyttäjän syöttämä merkkijono==5merkkiä pitkä, sekä string
            loop_wordle_5letters = False  # Ei voida isalpha() koska a-z

    return str.lower(arvaus)   #muuntaa isot kirjaimet pieniksi

def wordle_tulostus(color_code, checker, arvaus, loop, vastaus):
    win=False
    print(color_code[checker[0]] + f"[{arvaus[0]}]",
          color_code[checker[1]] + f"[{arvaus[1]}]",
          color_code[checker[2]] + f"[{arvaus[2]}]",  # tulostetaan rivi oikeine väreineen
          color_code[checker[3]] + f"[{arvaus[3]}]",
          color_code[checker[4]] + f"[{arvaus[4]}]" + reset)
    if checker[0] == "green" and checker[1] == "green" and checker[2] == "green" and \
            checker[3] == "green" and checker[4] == "green":
        loop = loop + 6
        print("Onnittelut voitosta!")
        win=True

    else:
        loop = loop + 1

    if loop >= 6 and win == False:
        print(f"Hävisit pelin, oikea sana oli {vastaus}")

    return loop, win

wordle_color_code = {
    "green": "\033[32m",
    "yellow": "\033[33m",   #tehdään dictionary josta saadaan oikea värin tunnus
    "reset": "\033[0m"
}

def ohjeet_wordle(green, yellow, reset):
    print("Terve tuloa pelaamaan wordle peliä!\n"
          "Tehtäväsi on arvata 5-kirjaiminen sana\n"
          "Arvauksen jälkeen näet mitkä kirjaimet olivat oikeita ja mitkä oikealla paikalla\n"
          "\n"
          "Sinulla on yhteensä 6 yritystä arvata sana\n"
          "\n"
          "Voit syöttää vain sanoja perus muodossa, ei esim monikkoja\n"
          "\n"
          "\n"
          "Esimerkki jossa vastaus on sana 'koira' ja olet arvannut 'ruoka' ja 'kissa':\n",
          yellow + "[r]", reset + "[u]", yellow + "[o]", yellow + "[k]", green + "[a]\n",
          green + "[k]", yellow + "[i]", reset + "[s]", "[s]", green + "[a]\n",
          reset + "\n"
                  "Kun olet valmis jatkamaan pelin syötä mikätahansa merkki")
    input("")
    print("Syötä ensimmäinen sana:")

def wordle(loop, green, yellow, reset):
    vastaus_wordle = vastaus_wordle_def() # määritellään wordle vastaus
    ohjeet_wordle(green, yellow, reset)
    while loop <6:
                                    # SanaApu.com
        arvaus=wordle_5letters()
        wordle_arvaus = wordle_arvaus_def(arvaus)  # määritellään pelaajan arvaus
        wordle_checker = checker_wordle(vastaus_wordle, wordle_arvaus)  # määritellään pelaajan syöttämän sanan tarkistus
        loop, voitto_wordle=wordle_tulostus(wordle_color_code, wordle_checker, wordle_arvaus, loop, vastaus_wordle) #Wordle tuloksen tulostus sekä loop tracking

    return voitto_wordle




green = "\033[32m"
yellow = "\033[33m"
reset = "\033[0m"
loop_wordle = 0

if __name__ == '__main__':
    wordle(loop_wordle, green, yellow, reset)

def arvaus_hirsipuu_def(arvattujenlista):
    sana_arvaus = False
    arvaus = input(f"Arvaa 1 kirjain tai koko sana:")
    arvaus = arvaus.upper()                             #pelaajan arvaus, hirsipuu

    if len(arvaus) >1:
        sana_arvaus = True
    else:
        arvattujenlista.append(arvaus)

    return arvaus, sana_arvaus, arvattujenlista




def difficulty_hirsipuu_def():
    loop = True

    while loop == True:
        difficulty = input("Valitse vaikeus taso, hard/easy")

        if difficulty == "easy":            #Vaikeuden valinta, hirsipuu
            loop=False
            difficulty = 1
        elif difficulty == "hard":
            loop=False
            difficulty = 0

    return difficulty


# hakee vastauksen sekä luo score pöydän
def vastaus_hirsipuu_def(difficulty):
    id = random.randint(1,103)
    score_table = []

    cursor.execute("SELECT sana_hard, sana_easy FROM hirsipuu WHERE id = %s", (id,))
    haettu_sana = cursor.fetchall()

    for i in range(len(haettu_sana[0][difficulty])):
        score_table.append("_")

    return haettu_sana[0][difficulty], score_table


def lettercheck_hirsipuu(vastaus, arvaus):
    kirjaimet = []
    tulos = []
    for i in vastaus:
        kirjaimet.append(i)

    for i in range(len(vastaus)):
        if arvaus == kirjaimet[i]:
            tulos.append(kirjaimet[i])
        else:
            tulos.append("_")

    return tulos


def finalscore_hirsipuu_def(roundscore, scoreboard):
    for i in range(len(scoreboard)):
        if scoreboard[i] == "_":
            scoreboard.append(roundscore[i])
        else:                                      #tekee uuden scoreboard
            scoreboard.append(scoreboard[i])

    for i in range(len(roundscore)):
        scoreboard.pop(0) #poistaa vanhat

    return scoreboard

def win_check_hirsipuu_def(arvaus, vastaus, loop, scoreboard):
    vastaus_list = list(vastaus)

    if arvaus in vastaus_list:
        loop = loop -1          #jos oikea kirjain niin kierros luku ei mene alaspäin

    if arvaus==vastaus or vastaus_list==scoreboard:
        win=True                                       #tarkistetaan onko pelaaja voittanut
    else:
        win=False

    return win, loop


def hirsipuu ():

    rightletter_hirsipuu = 0
    loop_hirsipuu = 0
    arvatut_kirjaimet_hirsipuu = []
    win_hirsipuu = False



    difficulty_hirsipuu = difficulty_hirsipuu_def()
    vastaus_hirsipuu, scoreboard_hirsipuu = vastaus_hirsipuu_def(difficulty_hirsipuu)

    while loop_hirsipuu < 10 and win_hirsipuu == False:

        arvaus_hirsipuu, is_answer, arvatut_kirjaimet_hirsipuu = arvaus_hirsipuu_def(
            arvatut_kirjaimet_hirsipuu)  # arvaus_hirsipuu = A-Ö tai sana, is_answer = boolean

        roundscore_hirsipuu = lettercheck_hirsipuu(vastaus_hirsipuu, arvaus_hirsipuu)
        scoreboard_hirsipuu = finalscore_hirsipuu_def(roundscore_hirsipuu, scoreboard_hirsipuu)

        win_hirsipuu, loop_hirsipuu = win_check_hirsipuu_def(arvaus_hirsipuu, vastaus_hirsipuu, loop_hirsipuu,
                                                             scoreboard_hirsipuu)
        loop_hirsipuu = loop_hirsipuu + 1

        if win_hirsipuu == False:
            print(f"{scoreboard_hirsipuu}<--Arvattava sana\n"
                  f"\n"
                  f"{arvatut_kirjaimet_hirsipuu}<--Arvatut kirjaimet\n"
                  f"\n"
                  f"\n"
                  f"Arvauksi jäljellä :{10 - loop_hirsipuu}")

    if win_hirsipuu == True:
        voitto = True
        print("Voitit pelin!")
    else:
        print(f"Hävisit pelin:(\n"
              f"Oikea vastaus oli {vastaus_hirsipuu}")
        voitto = False


location = "EFHK"
budget = 20000

player = None
while player == None:
    player = choose_player(location, budget)  #pelinimen valinta

print("Tervetuloa " + player + " pelaamaan lentokenttäappro peliä."
      "Tässä pelissä pääset matkaamaan lentokenttien välillä tehden minipelejä haalarimerkkejä varten."
      "Pelin voit voittaa kuluttamalla kaiken opintolainan ja onnistumalla saada tarpeeksi haalarimerkkejä.")

while budget > 0:
    connections= flight_paths(location)

    choise= flight_choise(connections, budget)

    budget, location = update_player(choise, player, budget)

    play_game()

print("Olet kuluttanut opintolainan loppuun")

def highscore():
    sql = """
    SELECT 
        screen_name AS "Pelaaja",
        COUNT(token_id) AS 'Merkkien määrä'
    FROM accomplishment
    JOIN player ON accomplishment.player_id = player.id
    GROUP BY player.id
    ORDER BY 'Merkkien määrä' DESC;
    """
    cursor.execute(sql)
    tulokset = cursor.fetchall()

    print("🏆 Highscore – kerätyt merkit")
    print("-" * 40)

    for pelaaja, maara in tulokset:
        print(f"{pelaaja:15} | {maara} merkkiä")

    cursor.close()
highscore()
