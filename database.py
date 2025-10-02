import mysql.connector
yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='lk_approt',
    user='kartsu',
    password='black_rose',
    autocommit=True
    )
cursor = yhteys.cursor()
# maria MD käskyjä
# update airport set minigame_id =
# (select id from minigame where name = "Numeron arvaus") where ident = "EFHK";

#cursor.execute("INSERT INTO player (budjet) VALUES (%s)",
              # ("100",) where name = "karo")
cursor.execute("CREATE TABLE IF NOT EXISTS connection ("
               "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
               "ident1 VARCHAR(40) NOT NULL,"
               "ident2 VARCHAR(40) NOT NULL,"
               "FOREIGN KEY(ident1) REFERENCES airport(ident)"
               "FOREIGN KEY(ident2) REFERENCES airport(ident)"
            )

