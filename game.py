import mysql.connector
import random
import sqlite3

yhteys = mysql.connector.connect(
    host="localhost",
    user="root",
    password="140305",
    autocommit=True,
    database="lk_approt",
    port=3306
)
cursor = yhteys.cursor()


# pelaajan valinta
def choose_player(location, budget):
    c = yhteys.cursor()

    nimi = input("Anna pelinimesi: ").strip()  # poistaa välilyönnit alusta ja lopusta
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

    sql = ("SELECT name, connection.price FROM airport "
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
        print(f"{i + 1}. {connections[i][0]} - {connections[i][1]}€")

    while True:
        choise = input("")
        if choise.isdigit():
            int_choise = int(choise)
            if int_choise <= len(connections):
                return connections[int(choise) - 1]

        print(f"Virhe! syötä kenttään vain kokonais luku väliltä 1-{len(connections)}.")


def update_player(tup, player, budget):
    c = yhteys.cursor()

    new_budget = budget - tup[1]
    airport = tup[0]

    # 1) Hae ICAO-ident (4-merkkinen)
    c.execute("SELECT ident FROM airport WHERE name = %s AND CHAR_LENGTH(ident) = 4", (airport,))
    row = c.fetchone()  # otetaan ensimmäinen rivi

    if row is None:
        print("Virhe: Ei löytynyt 4-merkkistä ICAO-koodia kentälle:", airport)
        new_location = None
    else:
        new_location = row[0]

        c.execute(
            "UPDATE player SET location=%s, budget=%s WHERE screen_name=%s",
            (new_location, new_budget, player)
        )


    c.close()
    return new_budget, new_location


def play_game(player):
    cursor = yhteys.cursor()

    sql = (
        "SELECT airport.ident, minigame.name FROM airport "
        "JOIN minigame ON airport.minigame_id = minigame.id "
        "JOIN player ON airport.ident = player.location "
        "WHERE player.screen_name = %s")

    cursor.execute(sql, (player,))
    tulos = cursor.fetchone()

    if tulos:
        location = tulos[0]
        minipelin_nimi = tulos[1]
        print(f"Pelaaja on kentällä {location}, minipeli on: {minipelin_nimi}")
        return minipelin_nimi
    else:
        print("Kentälle ei ole liitetty minipeliä.")
        return None


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
        return True
        print("Onneksi olkoon! Voitit pelin!")
    elif pelaajan_pisteet < tietokoneen_pisteet:
        print("Hävisit pelin!")
        return False
    else:
        print("Peli päättyi tasapeliin!")
        return False


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
                return True
        except ValueError:
            print("Ole hyvä ja syötä kokonaisluku.")


def wordle():
    def vastaus_wordle_def():
        wordle_id = [random.randint(1, 1426)]

        cursor.execute("SELECT sana from wordle WHERE id = %s", wordle_id)
        rows = cursor.fetchall()

        for (i,) in rows:
            vastaus = list(i)  # muutetaan vastaus listaksi jossa jokainen kirjain on yksi arvo

        return vastaus

    def checker_wordle(vastaus, arvaus_list):
        checker = []

        for i in range(5):
            if arvaus_list[i] == vastaus[i]:
                checker.append("green")
            elif arvaus_list[i] in vastaus:
                checker.append(
                    "yellow")  # laitetaan wordle_checker listaan jokaisen kirjaimen kohdalle oikea arvo (oikea paikka, oikea kirjain, väärin)
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

        return str.lower(arvaus)  # muuntaa isot kirjaimet pieniksi

    def wordle_tulostus(color_code, checker, arvaus, loop, vastaus):
        win = False
        print(color_code[checker[0]] + f"[{arvaus[0]}]",
              color_code[checker[1]] + f"[{arvaus[1]}]",
              color_code[checker[2]] + f"[{arvaus[2]}]",  # tulostetaan rivi oikeine väreineen
              color_code[checker[3]] + f"[{arvaus[3]}]",
              color_code[checker[4]] + f"[{arvaus[4]}]" + reset)
        if checker[0] == "green" and checker[1] == "green" and checker[2] == "green" and \
                checker[3] == "green" and checker[4] == "green":
            loop = loop + 6
            print("Onnittelut voitosta!")
            return loop, True

        else:
            loop = loop + 1

        if loop >= 6 and win == False:
            print(f"Hävisit pelin, oikea sana oli {vastaus}")

        return loop, win

    wordle_color_code = {
        "green": "\033[32m",
        "yellow": "\033[33m",  # tehdään dictionary josta saadaan oikea värin tunnus
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

    def wordle_peli(loop, green, yellow, reset):
        vastaus_wordle = vastaus_wordle_def()  # määritellään wordle vastaus
        ohjeet_wordle(green, yellow, reset)
        while loop < 6:
            # SanaApu.com
            arvaus = wordle_5letters()
            wordle_arvaus = wordle_arvaus_def(arvaus)  # määritellään pelaajan arvaus
            wordle_checker = checker_wordle(vastaus_wordle,
                                            wordle_arvaus)  # määritellään pelaajan syöttämän sanan tarkistus
            loop, voitto_wordle = wordle_tulostus(wordle_color_code, wordle_checker, wordle_arvaus, loop,
                                                  vastaus_wordle)  # Wordle tuloksen tulostus sekä loop tracking

        return voitto_wordle

    green = "\033[32m"
    yellow = "\033[33m"
    reset = "\033[0m"
    loop_wordle = 0

    win_wordle = wordle_peli(loop_wordle, green, yellow, reset)

    return win_wordle


def hirsipuu():
    def arvaus_hirsipuu_def(arvattujenlista):
        sana_arvaus = False
        arvaus = input(f"Arvaa 1 kirjain tai koko sana:")
        arvaus = arvaus.upper()  # pelaajan arvaus, hirsipuu

        if len(arvaus) > 1:
            sana_arvaus = True
        else:
            arvattujenlista.append(arvaus)

        return arvaus, sana_arvaus, arvattujenlista

    def difficulty_hirsipuu_def():
        loop = True

        while loop == True:
            difficulty = input("Valitse vaikeus taso, hard/easy")

            if difficulty == "easy":  # Vaikeuden valinta, hirsipuu
                loop = False
                difficulty = 1
            elif difficulty == "hard":
                loop = False
                difficulty = 0

        return difficulty

    # hakee vastauksen sekä luo score pöydän
    def vastaus_hirsipuu_def(difficulty):
        id = random.randint(1, 103)
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
            else:  # tekee uuden scoreboard
                scoreboard.append(scoreboard[i])

        for i in range(len(roundscore)):
            scoreboard.pop(0)  # poistaa vanhat

        return scoreboard

    def win_check_hirsipuu_def(arvaus, vastaus, loop, scoreboard):
        vastaus_list = list(vastaus)

        if arvaus in vastaus_list:
            loop = loop - 1  # jos oikea kirjain niin kierros luku ei mene alaspäin

        if arvaus == vastaus or vastaus_list == scoreboard:
            win = True  # tarkistetaan onko pelaaja voittanut
        else:
            win = False

        return win, loop

    def hirsipuu_game():

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
            return True
            print("Voitit pelin!")
        else:
            print(f"Hävisit pelin:(\n"
                  f"Oikea vastaus oli {vastaus_hirsipuu}")
            return False

    win = hirsipuu_game()

    return win


def blackjack():
    def init_db():
        conn = sqlite3.connect("blackjack.db")
        c = conn.cursor()

        c.execute("""
                  CREATE TABLE IF NOT EXISTS games
                  (
                      id
                      INTEGER
                      PRIMARY
                      KEY
                      AUTOINCREMENT,
                      result
                      TEXT,
                      player_hand
                      TEXT,
                      dealer_hand
                      TEXT
                  )
                  """)
        conn.commit()
        conn.close()

    def record_result(result, player_hand, dealer_hand):
        conn = sqlite3.connect("blackjack.db")
        c = conn.cursor()
        c.execute("INSERT INTO games (result, player_hand, dealer_hand) VALUES (?, ?, ?)",
                  (result, str(player_hand), str(dealer_hand)))
        conn.commit()
        conn.close()

    # BLACKJACK
    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    def card_value(card):
        if card in ["J", "Q", "K"]:
            return 10
        elif card == "A":
            return 11
        else:
            return int(card)

    def draw_card(deck):
        return deck.pop()

    def calculate_score(hand):
        score = sum(card_value(c) for c in hand)
        # jos yli 21 ja kädessä ässiä, vähennetään arvoa 11 -> 1
        aces = hand.count("A")
        while score > 21 and aces > 0:
            score -= 10  # muutetaan yksi ässä arvosta 11 -> 1
            aces -= 1
        return score

    def blackjack_game():
        # Luodaan korttipakka (52 korttia)
        deck = cards * 4
        random.shuffle(deck)

        player_hand = [draw_card(deck), draw_card(deck)]
        dealer_hand = [draw_card(deck), draw_card(deck)]

        # PELAAJAN VUORO
        while True:
            print(f"Pelaajan käsi: {player_hand} (arvo: {calculate_score(player_hand)})")
            if calculate_score(player_hand) > 21:
                print("Yli 21! Hävisit.")
                return "LOSE", player_hand, dealer_hand
            action = input("Otatko lisää (h) vai jäät (j)? ").lower()
            if action == "h":
                player_hand.append(draw_card(deck))
            else:
                break

        # JAKAJAN VUORO
        while calculate_score(dealer_hand) < 17:
            dealer_hand.append(draw_card(deck))

        player_score = calculate_score(player_hand)
        dealer_score = calculate_score(dealer_hand)

        print(f"Jakajan käsi: {dealer_hand} (arvo: {dealer_score})")

        if dealer_score > 21 or player_score > dealer_score:
            print("Voitit!")
            return True, player_hand, dealer_hand
        elif player_score == dealer_score:
            print("Tasapeli.")
            return "DRAW", player_hand, dealer_hand
        else:
            print("Hävisit.")
            return False, player_hand, dealer_hand

    # MAIN
    if __name__ == "__main__":
        init_db()
        result, player_hand, dealer_hand = blackjack_game()
        record_result(result, player_hand, dealer_hand)


def matikkavisa():
    kysymykset = {
        "5 + 3": 8,
        "9 - 4": 5,
        "7 * 2": 14,
        "12 / 3": 4,
        "8 + 6": 14,
        "15 - 7": 8,
        "4 * 5": 20,
        "20 / 4": 5,
        "10 + 9": 19,
        "14 - 6": 8,
        "6 * 3": 18,
        "18 / 2": 9,
        "11 + 8": 19,
        "13 - 9": 4,
        "9 * 4": 36,
        "24 / 6": 4,
        "16 + 7": 23,
        "25 - 12": 13,
        "5 * 8": 40,
        "30 / 5": 6}

    valitut_kysymykset = random.sample(list(kysymykset.items()), 5)

    print("Tervetuloa pelaamaan! Vastaa viiteen kysymykseen oikein voittaaksesi.")
    print("Jos vastaat väärin, peli loppuu heti.")

    # PELI
    for kysymys, vastaus in valitut_kysymykset:
        try:
            user_input = float(input(f"{kysymys} = "))
        except ValueError:
            print("Virheellinen syöte.")
            break
        if user_input != vastaus:
            print(f"Väärin! Oikea vastaus on {vastaus}. Hävisit pelin.")
            return False
    else:
        print("Onneksi olkoon! Vastasit kaikki oikein ja voitit pelin.")
        return True


def tarina(location):
    sql = 'SELECT story FROM stories WHERE ident = %s'
    kursori = yhteys.cursor()
    kursori.execute(sql, (location,))
    story = kursori.fetchall()
    kursori.close()
    return story


def token(location, player):
    cursor = yhteys.cursor()
    try:
        # Haetaan pelaajan ja tokenin ID:t
        cursor.execute("SELECT id FROM player WHERE screen_name = %s", (player,))
        player_row = cursor.fetchone()

        cursor.execute("SELECT token_id FROM airport WHERE ident = %s", (location,))
        token_row = cursor.fetchone()

        if not player_row or not token_row:
            print("Tokenia tai pelaajaa ei löytynyt.")
            return

        player_id = player_row[0]
        token_id = token_row[0]

        cursor.execute("""
            SELECT 1 FROM accomplishment 
            WHERE player_id = %s AND token_id = %s
        """, (player_id, token_id))

        if cursor.fetchone():
            print(f"Sinulla on jo tämä token ({token_id}) kentältä {location}.")
        else:
            cursor.execute("""
                INSERT INTO accomplishment (player_id, token_id)
                VALUES (%s, %s)
            """, (player_id, token_id))
            print(f"Lisätty uusi token pelaajalle {player} sijainnissa {location}!")

        yhteys.commit()

    except Exception as e:
        yhteys.rollback()
        print("Virhe tokenin käsittelyssä:", e)

    finally:
        cursor.close()

# ---------------------------------------

location = "EFHK"
budget = 20000

player = None
while player == None:
    player = choose_player(location, budget)  # pelinimen valinta

print("Tervetuloa " + player + " pelaamaan lentokenttäappro peliä."
                               " Tässä pelissä pääset matkaamaan lentokenttien välillä tehden minipelejä haalarimerkkejä varten."
                               " Pelin voit voittaa kuluttamalla kaiken opintolainan ja onnistumalla saada tarpeeksi haalarimerkkejä.")

while budget > 0:
    connections = flight_paths(location)

    choise = flight_choise(connections, budget)

    budget, location = update_player(choise, player, budget)

    tarina(location)

    minipeli = play_game(player)
    if minipeli == "Kivi_sakset_paperi":
        win = kivi_sakset_paperi()
    elif minipeli == "Matikkavisa":
        win = matikkavisa()
    elif minipeli == "Blackjack":
        win = blackjack()
    elif minipeli == "Wordle":
        win = wordle()
    elif minipeli == "Numeron arvaus":
        win = numeron_arvauspeli()
    elif minipeli == "Hirsipuu":
        win = hirsipuu()
    else:
        win = False

    if win:
        token(location, player)
    else:
        print("Et saanut tokenia tällä kertaa.")

print("Olet kuluttanut opintolainan loppuun")


def highscore():
    sql = """
          SELECT screen_name AS "Pelaaja", \
                 COUNT(token_id) AS 'Merkkien määrä'
          FROM accomplishment
                   JOIN player ON accomplishment.player_id = player.id
          GROUP BY player.id
          ORDER BY COUNT(token_id) DESC; \
          """
    cursor.execute(sql)
    tulokset = cursor.fetchall()

    print("🏆 Highscore – kerätyt merkit")
    print("-" * 40)

    for pelaaja, maara in tulokset:
        print(f"{pelaaja:15} | {maara} merkkiä")


highscore()