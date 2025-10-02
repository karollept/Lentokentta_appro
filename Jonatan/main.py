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

#Etsii lento yhteydet
def flight_path(location):
    c= yhteys.cursor()
    c.execute("SELECT kenttä.nimi FROM kenttä "
              "INNER JOIN yhteys ON kenttä.id=yhteys.yhteys_id "
              "WHERE yhteys.kenttä_id=(%s)",
              (location,))

    tulos = c.fetchall()
    c.close()

    print("Valitse minne haluat lentää:")
    for i in range(len(tulos)):
        print(f"{i+1}.{tulos[i][0]}")
    return tulos


def flight_choise(options, loop):

    while loop ==True:
        choise = input("")
        if choise not in ("1", "2", "3"):
            print("Syötä kenttään vain 1 , 2 tai 3")
        else:
            loop = False

    airport_choise = options[int(choise)-1]
    return airport_choise

def chosen_airport_id(airport):
    c = yhteys.cursor()

    c.execute("SELECT kenttä.id FROM kenttä "
              "WHERE kenttä.nimi = (%s)",
              airport)
    tulos = c.fetchone()
    c.close()
    return tulos[0]

def_loop = True

player = None
while player == None:
    player = choose_player()

print(player)


location = 1
main_loop = True
while main_loop == True:

    yhteydet=flight_path(location)
    valittu_kenttä=flight_choise(yhteydet, def_loop)

    location=chosen_airport_id(valittu_kenttä)



