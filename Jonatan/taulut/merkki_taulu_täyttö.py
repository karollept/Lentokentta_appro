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

merkit = """keltainen vihreä sininen punainen pinkki
"""
merkki_lista = []

for i in merkit.split():
    merkki_lista.append(i)

for i in range(len(merkki_lista)):
    cursor.execute("INSERT INTO merkki (nimi) VALUES (%s)",
                   (merkki_lista[i],))
