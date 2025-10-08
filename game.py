import mysql.connector
import random


yhteys = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "f3V3r_dr34m3r",
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

def play_game(location):
    cursor = yhteys.cursor()

    sql= ("SELECT minigame.name FROM airport "
          "JOIN minigame ON airport.minigame_id = minigame.id"
          " WHERE ident = %s")

    cursor.execute(sql, (location,))
    tulos = cursor.fetchone()

    if tulos:
        minipelin_nimi = tulos[0]
        print(f"Pelaaja on kentällä {location}, minipeli on: {minipelin_nimi}")
        return minipelin_nimi
    else:
        print(f"Kentälle {location} ei ole liitetty minipeliä.")
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
        won = True
        print("Onneksi olkoon! Voitit pelin!")
    elif pelaajan_pisteet < tietokoneen_pisteet:
        print("Hävisit pelin!")
        won = False
    else:
        print("Peli päättyi tasapeliin!")
        won = False


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