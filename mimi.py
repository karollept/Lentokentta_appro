import mysql.connector


yhteys = mysql.connector.connect(
    host="localhost",
    user="root",
    password = "f3V3r_dr34m3r",
    autocommit = True,
    db = "lk_approt",
    port = 3306
)
cursor = yhteys.cursor()

def highscore():
    sql = """
    SELECT 
        screen_name AS "Pelaaja",
        COUNT(token_id) AS "Merkkien määrä"
    FROM accomplishment
    JOIN player ON player_id = id
    GROUP BY player.id
    ORDER BY "Merkkien määrä" DESC;
    """
    cursor.execute(sql)
    tulokset = cursor.fetchall()
    print("🏆 Highscore – kerätyt merkit")
    print("-" * 40)

    for pelaaja, maara in tulokset:
        print(f"{pelaaja:15} | {maara} merkkiä")
    cursor.close()