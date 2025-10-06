'''
Tietokanta luonti skripti.
Kaikki Foreign keyt sekä primaryt määritelty yms
Python näyttää jostain syystä keltaisella, ei kenties ymmärrä MariaDB kieltä
'''


import mysql.connector

'''
Kaikki oikeudet tulee ensin antaa root käyttäjällä-> omalle käyttäjälleen
GRANT ALL PRIVILEGES ON flight_game.* TO 'JonatanGM'@'localhost'; 
Tämä tulee tehdä ensin mariaDB flight_game sisällä
Jos ei toimi niin myös FLUSH PRIVILIGES; tämän jälkeen
'''

yhteys = mysql.connector.connect(
    host="localhost",
    user="JonatanGM",
    password = "123",
    autocommit = True,
    port = 3306
)
cursor = yhteys.cursor()

cursor.execute("USE flight_game")
'''
Luodaan nyt taulut, oli ongelmia foreign keyn yhdistyksessä airport taulun ident sarakkeeseen
korjaus oli: ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci
Löytää komennolla SHOW CREATE TABLE airport;
Kaikki tulee siis olla foreign keyn ja primaryn välillä samaa 
'''

# DEBUG, poistaa kaikki luodut tablet halutessa kun ilmenee virheitä:
debug = input("paina '1' poistaaksesi\n"
              "mitä vain muuta jatkaaksesi")
if debug == "1":
    cursor.execute("DROP TABLE IF EXISTS omistaa")
    cursor.execute("DROP TABLE IF EXISTS inventory")
    cursor.execute("DROP TABLE IF EXISTS merkit")
    cursor.execute("DROP TABLE IF EXISTS pelaaja")    # Taulut tulee pudottaa oikeassa järjestyksessä.


#pelaaja taulu
cursor.execute("CREATE TABLE IF NOT EXISTS pelaaja ("
               "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
               "nimi VARCHAR(40) NOT NULL,"
               "airport_id VARCHAR(40) DEFAULT NULL,"
               "FOREIGN KEY(airport_id) REFERENCES airport(ident)"
")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;"
            )

#inventory taulu
cursor.execute("CREATE TABLE IF NOT EXISTS inventory ("
               "id INT AUTO_INCREMENT PRIMARY KEY,"
               "raha INT NOT NULL DEFAULT 5000,"
               "pelaaja_id INT,"
               "FOREIGN KEY (pelaaja_id) REFERENCES pelaaja(id)" #inventory.pelaaja_id=pelaaja.id
")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;" #laitetaan kaikkiin tauluihin nämä:
               )                                                   #ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci
                                                                   #jotta foreign keyt toimivat kunnolla eikä tule tulevaisuudessa ongelmia.
#haalari_merkit taulu
# Tämä täytyy luoda ennen omistaa, koska omistaa taulu vaatii foreign keyn yhdistämistä haalari_merkit tauluun.
# muutetaan samalla nimi haalari_merkit->merkit ja myöhemmin omistaa.haalari_id->merkit_id

cursor.execute("CREATE TABLE IF NOT EXISTS merkit ("  #IF NOT EXISTS on tarpeen testausten vuoksi jotei kopioita ilmene.
               "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,"
               "nimi VARCHAR(40) NOT NULL"
               ")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;"
               )

# omistaa taulu   ----  omistaa.haalari_id -> merkit_id

cursor.execute("CREATE TABLE IF NOT EXISTS omistaa ("
               "merkit_id INT NOT NULL,"
               "pelaaja_id INT NOT NULL,"
               "PRIMARY KEY (merkit_id, pelaaja_id),"   # Ei antanut tehdä erikseen. Yhdistetty avain ei anna useampaa merkkiä yhdelle pelaajalle. en löytänyt muuta vaihtoehtoa.      
               "FOREIGN KEY (merkit_id) REFERENCES merkit(id),"
               "FOREIGN KEY (pelaaja_id) REFERENCES pelaaja(id)"
               ")ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;"
               )


# Testataan toimiiko tietokanta oikein luomalla muutamat arvot

#merkit:
cursor.execute("INSERT INTO merkit (nimi) VALUES (%s)",
               ("punainen",))
cursor.execute("INSERT INTO merkit (nimi) VALUES (%s)",   #laitetaan "x", jotta saadaan tuple
               ("sininen",))
cursor.execute("INSERT INTO merkit (nimi) VALUES (%s)",
               ("keltainen",))
#pelaaja
cursor.execute("INSERT INTO pelaaja (nimi) VALUES (%s)",
               ("Jonatan",))

cursor.execute("SELECT pelaaja.id FROM pelaaja where nimi=%s", ("Jonatan",))
pelaaja_id = cursor.fetchone()[0]  # valitaan aluksi oikea pelaaja id inventorya varten

#inventory
cursor.execute("INSERT INTO inventory (pelaaja_id, raha) VALUES (%s, %s)",
               (pelaaja_id, 5000)
               )

#omistaa
#Etsitään tätä varten myös keltainen merkin id
cursor.execute("SELECT merkit.id FROM merkit WHERE nimi=%s",
               ("keltainen",))
merkit_id = cursor.fetchone()[0]

cursor.execute("INSERT INTO omistaa (merkit_id, pelaaja_id) VALUES (%s,%s)", # (%, %) tarkoittaa yhtä riviä jossa on kaksi saraketta
               (merkit_id, pelaaja_id))

cursor.execute("""
SELECT pelaaja.nimi, merkit.nimi, inventory.raha
FROM inventory
INNER JOIN pelaaja ON inventory.pelaaja_id=pelaaja.id
INNER JOIN omistaa ON pelaaja.id=omistaa.pelaaja_id
INNER JOIN merkit ON omistaa.merkit_id=merkit.id
WHERE pelaaja.nimi='Jonatan';
""")

tulos=cursor.fetchall()
print(tulos)

