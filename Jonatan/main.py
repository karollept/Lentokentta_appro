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
def pelaajan_valinta():
    c= yhteys.cursor()
    nimi = input("Anna pelinimesi: ")

    vapaa = nimi_check(nimi)

    if vapaa == None:
        c.execute("INSERT INTO pelaaja (nimi) VALUES (%s)",
                    (nimi,))
        c.close()
        return True
    else:
        print("Pelaaja nimi varattu, valitse toinen")
        return False


def nimi_check(nimi):
    c = yhteys.cursor()
    c.execute("SELECT nimi FROM pelaaja WHERE nimi = (%s)",
               (nimi,))
    tulos = c.fetchall()

    c.close()

    return tulos[0] if len(tulos) > 1 else None


def lento_valinta():
    print("Valitse seuraavaksi mille kentälle haluat lentää")


while pelaajan_valinta() == False:
    pelaajan_valinta()

lento_valinta()

