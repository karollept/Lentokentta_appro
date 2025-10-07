import mysql.connector
import random
yhteys = mysql.connector.connect(
    host="localhost",
    user="JonatanGM",    # vaihda omanimi
    password = "123",    # vaihda oma salasana
    autocommit = True,
    port = 3306
)
cursor = yhteys.cursor()

cursor.execute("USE flight_game")




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