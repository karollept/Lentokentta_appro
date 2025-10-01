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

debug = input("paina '1' poistaaksesi\n"
              "mitä vain muuta jatkaaksesi")
if debug == "1":
    cursor.execute("DROP TABLE IF EXISTS pelaaja")

cursor.execute("CREATE TABLE IF NOT EXISTS pelaaja ("
               "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
               "nimi VARCHAR(40) NOT NULL,"
               "raha INT NOT NULL DEFAULT 25000,"
               "location VARCHAR(40) DEFAULT NULL,"
               
               "FOREIGN KEY(location) REFERENCES airport(ident)"
")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;"
            )

cursor.execute("CREATE TABLE IF NOT EXISTS merkki ("
               "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
               "nimi VARCHAR(40) NOT NULL"

               ")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;"
               )

cursor.execute("CREATE TABLE IF NOT EXISTS omistaa ("
               "pelaaja_id INT NOT NULL,"
               "merkki_id INT NOT NULL,"
               "PRIMARY KEY (pelaaja_id, merkki_id),"

               "FOREIGN KEY(pelaaja_id) REFERENCES pelaaja(id),"
               "FOREIGN KEY(merkki_id) REFERENCES merkki(id)"
               ")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;"
               )


