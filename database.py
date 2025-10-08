import mysql.connector
yhteys = mysql.connector.connect(
    host='localhost',
    port= 3306,
    database='lk_approt',
    user='user',          #your password
    password='password',  #your password
    autocommit=True
    )
cursor = yhteys.cursor()
maria MD käskyjä
update airport set minigame_id =
(select id from minigame where name = "Numeron arvaus") where ident = "EFHK";

updateminigame
set name = 'Kivi_sakset_paperi'
where name = 'kivi-sakset-paperi';  #koska sen pitää match miten koodissa lukee

cursor.execute("INSERT INTO player (budget) VALUES (%s)",
              ("1000",) where name = "karo")


