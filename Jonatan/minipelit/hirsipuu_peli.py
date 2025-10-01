import mysql.connector
import random


yhteys = mysql.connector.connect(
    host= 'localhost',
    user='JonatanGM',
    password='123',
    port=3306,
    autocommit=True
)

cursor=yhteys.cursor()

cursor.execute("USE flight_game")

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
        print("Voitit pelin!")
    else:
        print(f"Hävisit pelin:(\n"
              f"Oikea vastaus oli {vastaus_hirsipuu}")



hirsipuu()






