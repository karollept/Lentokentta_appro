import mysql.connector


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


location = "EFHK"
budget = 20000

player = None
while player == None:
    player = choose_player(location, budget)  #pelinimen valinta

print("Tervetuloa " + nimi + " pelaamaan lentokenttäappro peliä."
      "Tässä pelissä pääset matkaamaan lentokenttien välillä tehden minipelejä haalarimerkkejä varten."
      "Pelin voit voittaa kuluttamalla kaiken opintolainan ja onnistumalla saada tarpeeksi haalarimerkkejä.")

while budget > 0:
    connections= flight_paths(location)

    choise= flight_choise(connections, budget)

    budget, location = update_player(choise, player, budget)

print("Olet kuluttanut opintolainan loppuun")
