import mysql.connector

yhteys = mysql.connector.connect(
         host='127.0.0.1',
         database='lk_approt',
         user='aleksi',
         password='koivunoksa32',
         autocommit=True
         )

def tarina(koodi):
    sql = 'SELECT story FROM stories WHERE country = %s'
    kursori = yhteys.cursor()
    kursori.execute(sql, (koodi,))
    tulos = kursori.fetchall()
    return tulos

code = input("Syötä Euroopan maa: ")
story = tarina(code)

print(story)