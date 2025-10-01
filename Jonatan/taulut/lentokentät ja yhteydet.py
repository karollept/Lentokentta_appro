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

cursor.execute("DROP TABLE IF EXISTS yhteydet")
cursor.execute("DROP TABLE IF EXISTS kenttä")

cursor.execute("CREATE TABLE IF NOT EXISTS kenttä ("
               "nimi VARCHAR(100) NOT NULL,"
               "id INT NOT NULL AUTO_INCREMENT PRIMARY KEY"
               ")ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
               )


kentät = """Helsinki-Vantaa
Tukholma
Kööpenhamina
Tallinna
Schipholin
Andorra–La Seu d'Urgell
Ankara Esenboga
Eleftherios Venizelosin
Baku International Airport
Belgrade Nikola Tesla Airport
Berlin Brandenburg Airport
M. R. Stefanik Airport
Bern Airport
Brussels Airport
Budapest Ferenc Liszt Intl Airport
Henri Coandă International Airport
Chișinău International Airport
Dublin Airport
Zvartnots International Airport
Boryspil International Airport
Humberto Delgado Airport
Ljubljana Jože Pučnik Airport
Heathrow Airport
Luxembourg Airport
Adolfo Suárez Madrid–Barajas Airport
Minsk National Airport
Sheremetyevo International Airport
Larnaca International Airport
Oslo Gardermoen Airport
Václav Havel Airport Prague
Charles de Gaulle Airport
Podgorica Airport
Pristina International Airport
Keflavík International Airport
Riga International Airport
Leonardo da Vinci–Fiumicino Airport
Sarajevo International Airport
Skopje International Airport
Sofia Airport
Tbilisi International Airport
Tirana International Airport (Nënë Tereza)
Malta International Airport
Warsaw Chopin Airport
Vilnius Airport
Vienna International Airport
Franjo Tuđman Airport
"""
kenttä_lista=[]

for i in kentät.splitlines():
    kenttä_lista.append(i)

for i in range(len(kenttä_lista)):
    cursor.execute("INSERT INTO kenttä (nimi) VALUES (%s)",
                   (kenttä_lista[i],))


yhteydet = [
    (1, 2), (1, 3), (1, 4),             # Helsinki-Vantaa
    (2, 1), (2, 29), (2, 11),           # Tukholma
    (3, 1), (3, 34), (3, 43),           # Kööpenhamina
    (4, 1), (4, 35), (4, 44),           # Tallinna
    (5, 11), (5, 14), (5, 45),          # Schipholin
    (6, 31), (6, 25), (6, 23),          # Andorra–La Seu d'Urgell
    (7, 28), (7, 40), (7, 27),          # Ankara Esenboga
    (8, 28), (8, 41), (8, 38),          # Eleftherios Venizelosin
    (9, 40), (9, 27), (9, 19),          # Baku International Airport
    (10, 33), (10, 37), (10, 20),       # Belgrade Nikola Tesla Airport
    (11, 2), (11, 5), (11, 14),         # Berlin Brandenburg Airport
    (12, 30), (12, 15), (12, 17),       # M. R. Stefanik Airport
    (13, 45), (13, 24), (13, 28),       # Bern Airport
    (14, 5), (14, 11), (14, 46),        # Brussels Airport
    (15, 12), (15, 39), (15, 16),       # Budapest Ferenc Liszt Intl Airport
    (16, 25), (16, 20), (16, 15),       # Henri Coandă International Airport
    (17, 20), (17, 25), (17, 12),       # Chișinău International Airport
    (18, 34), (18, 23), (18, 21),       # Dublin Airport
    (19, 9), (19, 40), (19, 24),        # Zvartnots International Airport
    (20, 17), (20, 16), (20, 10),       # Boryspil International Airport
    (21, 42), (21, 25), (21, 18),       # Humberto Delgado Airport
    (22, 46), (22, 36), (22, 35),       # Ljubljana Jože Pučnik Airport
    (23, 6), (23, 18), (23, 30),        # Heathrow Airport
    (24, 31), (24, 13), (24, 19),       # Luxembourg Airport
    (25, 6), (25, 21), (25, 17),        # Adolfo Suárez Madrid–Barajas Airport
    (26, 35), (26, 27), (26, 16),       # Minsk National Airport
    (27, 26), (27, 9), (27, 7),         # Sheremetyevo International Airport
    (28, 7), (28, 8), (28, 13),         # Larnaca International Airport
    (29, 2), (29, 34), (29, 44),        # Oslo Gardermoen Airport
    (30, 12), (30, 43), (30, 23),       # Václav Havel Airport Prague
    (31, 6), (31, 24), (31, 42),        # Charles de Gaulle Airport
    (32, 33), (32, 39), (32, 37),       # Podgorica Airport
    (33, 41), (33, 32), (33, 10),       # Pristina International Airport
    (34, 3), (34, 18), (34, 29),        # Keflavík International Airport
    (35, 4), (35, 26), (35, 22),        # Riga International Airport
    (36, 45), (36, 41), (36, 22),       # Leonardo da Vinci–Fiumicino Airport
    (37, 10), (37, 38), (37, 32),       # Sarajevo International Airport
    (38, 8), (38, 37), (38, 39),        # Skopje International Airport
    (39, 32), (39, 15), (39, 38),       # Sofia Airport
    (40, 9), (40, 19), (40, 7),         # Tbilisi International Airport
    (41, 8), (41, 36), (41, 33),        # Tirana International Airport
    (42, 21), (42, 46), (42, 31),       # Malta International Airport
    (43, 3), (43, 44), (43, 30),        # Warsaw Chopin Airport
    (44, 43), (44, 4), (44, 29),        # Vilnius Airport
    (45, 13), (45, 36), (45, 5),        # Vienna International Airport
    (46, 14), (46, 22), (46, 42)        # Franjo Tuđman Airport
]
cursor.execute("CREATE TABLE IF NOT EXISTS yhteydet ("
               "id INT AUTO_INCREMENT PRIMARY KEY,"
               "yhteys_id INT NOT NULL,"
               "kenttä_id INT NOT NULL,"
               "FOREIGN KEY (kenttä_id) REFERENCES kenttä(id),"
               "FOREIGN KEY (yhteys_id) REFERENCES kenttä(id)"
               ")ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;"
               )

for i in range(len(yhteydet)):
    cursor.execute("INSERT INTO yhteydet (kenttä_id, yhteys_id) VALUES (%s, %s)",
                   (yhteydet[i]))
