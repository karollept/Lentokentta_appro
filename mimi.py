import mysql.connector


yhteys = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "salasana",
    autocommit = True,
    db = "lk_approt",
    port = 3306
)
cursor = yhteys.cursor()

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


def play_game():
    cursor = yhteys.cursor()

    sql = (
        "SELECT airport.ident, minigame.name FROM airport "
        "JOIN minigame ON airport.minigame_id = minigame.id "
        "JOIN player ON airport.ident = player.location "
        "WHERE player.id = 6"
    )

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
        won = True
        print("Onneksi olkoon! Voitit pelin!")
    elif pelaajan_pisteet < tietokoneen_pisteet:
        print("Hävisit pelin!")
        won = False
    else:
        print("Peli päättyi tasapeliin!")
        won = False
    return won
play_game()
