import mysql.connector


yhteys = mysql.connector.connect(
    host="localhost",
    user="JonatanGM",
    password = "123",
    autocommit = True,
    port = 3306
)
cursor = yhteys.cursor()

cursor.execute("USE flight_game")

#pelaajan valinta
def choose_player():
    c= yhteys.cursor()

    nimi = input("Anna pelinimesi: ").strip()  #poistaa välilyönnit alusta ja lopusta
    if nimi == "":
        print("Tyhjää merkkijona ei hyväksytä.")
        return None


    vapaa = is_name_taken(nimi)

    if vapaa == None:
        c.execute("INSERT INTO pelaaja (nimi) VALUES (%s)",
                    (nimi,))
        c.close()
        return nimi

    else:
        print("Pelaaja nimi varattu, valitse toinen")
        return None


def is_name_taken(nimi):
    c = yhteys.cursor()
    c.execute("SELECT nimi FROM pelaaja WHERE nimi = (%s)",
               (nimi,))
    tulos = c.fetchall()

    c.close()

    return tulos[0] if len(tulos) > 0 else None



player = None
while player == None:
    player = choose_player()  #pelinimen valinta




import wordle_peli

green = "\033[32m"
yellow = "\033[33m"
reset = "\033[0m"
loop_wordle = 0

win_wordle=wordle_peli.wordle(loop_wordle, green, yellow, reset)
