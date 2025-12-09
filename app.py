from logging import raiseExceptions

from flask import Flask, render_template, jsonify, request, session, make_response
import mysql.connector
import random

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="140305",
        database="lk_approt",
        port=3306
    )
app = Flask(__name__)
app.secret_key = 'sala_sana'
difficulty = "hard"


# Tämä muuttuja saa arvon True jos wordle voitetaan
minigame_win = False
hirsipuu_win = False

def get_flight_price(location, destination):
    sql = "SELECT price FROM connection WHERE ident1 = %s AND ident2 = %s"

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql, (location, destination))
    result = cursor.fetchone()
    cursor.close()

    if result:
        return result[0]
    else:
        return None

def get_minigame_for_player():
    location = session.get('location')
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT m.name FROM airport a JOIN minigame m ON a.minigame_id = m.ID WHERE a.ident = %s", (location,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result[0]  # minipelin nimi
    return None

def minigame_select(minigame):
    if minigame is not None:
        if minigame == "Wordle":
            return render_template("wordle.html")
        elif minigame == "Hirsipuu":
            return render_template("hirsipuu.html")
        elif minigame == "Numeron arvaus":
            return render_template("game.html")
        elif minigame == "Kivi_sakset_paperi":
            return render_template("game.html")
        elif minigame == "Matikkavisa":
            return render_template("game.html")
        elif minigame == "Blackjack":
            return render_template("game.html")
    return None

def get_player_data():
    yhteys = get_connection()
    cursor = yhteys.cursor()

    cursor.execute("select location, budget from player where id  = %s", (session['player_id'],))
    result = cursor.fetchall()

    if result:
        cursor.close()
        yhteys.close()

    return result

def update_player_data():
    location = session.get('location')
    budget = session.get('budget')

    yhteys = get_connection()
    cursor = yhteys.cursor()

    sql = "UPDATE player SET location = %s, budget = %s WHERE id = %s"
    cursor.execute(sql, (location, budget, session['player_id']))
    yhteys.commit()
    cursor.close()
    yhteys.close()


def update_token():
    yhteys = None
    cursor = None
    try:
        yhteys = get_connection()
        cursor = yhteys.cursor()

        location = session.get('location')
        player_id = session.get('player_id')

        # 1. HAE TOKENIN ID nykyisen sijainnin perusteella
        select_sql = "SELECT token_id FROM airport WHERE ident = %s"
        cursor.execute(select_sql, (location,))
        result = cursor.fetchone()

        token_id = result[0]

        # 2. TARKISTA ONKO TOKEN JO OLEMASSA
        check_sql = "SELECT 1 FROM accomplishment WHERE player_id = %s AND token_id = %s"
        cursor.execute(check_sql, (player_id, token_id))

        if cursor.fetchone():
            print(f"Token ID {token_id} on jo pelaajalla {player_id}")
            return True

            # 3. LISÄÄ TOKEN ACCOMPLISHMENT-TAULUUN
        insert_sql = "INSERT INTO accomplishment (player_id, token_id) VALUES (%s, %s)"
        cursor.execute(insert_sql, (player_id, token_id))

        # 4. VAHVISTA MUUTOS
        yhteys.commit()
        print(f"Token ID {token_id} lisätty pelaajalle {player_id}.")
        return True

    except mysql.connector.Error as err:
        print("Virhe tokenin lisäyksessä: ", err)
        if yhteys:
            yhteys.rollback()
        return False

    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()

# käytä tämä funktio sijainnin päivittymisen jälkeen uuteen.
def get_story():
    location = session.get('location')

    try:
        yhteys = get_connection()
        cursor = yhteys.cursor()

        sql= "SELECT story FROM stories WHERE stories.ident = %s"
        cursor.execute(sql, (location,))
        story = cursor.fetchone()

    except mysql.connection.Error as err:
        if yhteys:
            yhteys.rollback()
        else: return False

    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()

    return story[0]

    # Projektin etusivu
@app.route("/")
def home():#

    # Pelaajan id
    session['player_id'] = 14
    stats = get_player_data()
    print(stats)
    # Pelaajan sijainti
    if stats and len(stats) >= 2:

        session['location'] = stats[0][0]
        # Pelaajan budjetti
        session['budget'] = stats[0][1]
    else:
        session['location'] = "EFHK"
        session['budget'] = 0

    # Kierrosnumero
    session['round'] = 1

    return render_template("index.html")

# Wordle-sivun reitti
@app.route("/wordle")
def wordle():
    return render_template("wordle.html")


@app.route("/wordle/get_value")
def wordle_api():
    tunnus = random.randint(1, 1420)
    try:
        yhteys = get_connection()
        cursor = yhteys.cursor()
        query = "select sana from wordle where id = %s"
        cursor.execute(query, (tunnus,))
        result = cursor.fetchone()

    except mysql.connector.Error as err:
        print("Virhe: " , err)
    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()

    if result:
        return jsonify({"value": result})
    return None


@app.route("/minigame/check", methods=['POST'])
def minigame_check():
    global minigame_win
    data = request.get_json()

    minigame_win = bool(data['value'])
    print("minigame_win = ", minigame_win)

    if minigame_win:
        update_token()
    update_player_data()

    return jsonify({"status": "ok", "win_state": minigame_win})


@app.route("/hirsipuu")
def hirsipuu():
    response = make_response(render_template("hirsipuu.html"))

    #Selaimen välimuisti esto
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response
@app.route("/hirsipuu/get_value")
def hirsipuu_api():
    tunnus = random.randint(1, 103)
    global difficulty
    col = "sana_" + difficulty
    query = f"SELECT {col} FROM hirsipuu WHERE id = %s"

    try:
        yhteys = get_connection()
        cursor = yhteys.cursor()
        print(query)
        cursor.execute(query, (tunnus,))

        result = cursor.fetchone()
    except mysql.connector.Error as err:
        print("Virhe: " , err)
    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()
    if result:
        return jsonify({"value": result})
    return None


@app.route("/hirsipuu/set_value", methods=['POST'])
def set_value_hirsipuu():
    global hirsipuu_win
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({"error": "No value provided"}), 400

    hirsipuu_win = bool(data['value'])
    print("hirsipuu = ", hirsipuu_win)
    return jsonify({"status": 'ok', 'received': hirsipuu_win})


#Haalarimerkki kokoelma sivu

@app.route("/haalarimerkit")
def haalarimerkki():
    return render_template("haalarimerkit.html")
@app.route("/haalarimerkki/get_value")
def haalarimerkki_api():

    try:
        yhteys = get_connection()
        cursor = yhteys.cursor()
        player_id = session.get('player_id')
        query = "SELECT token.name FROM token INNER JOIN accomplishment ON accomplishment.token_id = token.id WHERE accomplishment.player_id = %s"
        cursor.execute(query, (player_id,))
        result = cursor.fetchall()
        print(result)
    except mysql.connector.Error as err:
        print("Virhe: " , err)
    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()
    if result:
        names = []
        for row in result:
            names.append(row[0])
        return jsonify(names)
    return None

@app.route("/game")
def game():
    return render_template("game.html")

@app.route("/game/get_yhteydet")
def game_get_yhteydet():
    try:
        yhteys = get_connection()
        cursor = yhteys.cursor()

        sql = "select ident1 from connection where ident2 = %s"
        location = session.get('location', 'EFHK')
        cursor.execute(sql, (location,))
        result = cursor.fetchall()


        listOfDicts = []
        for row in result:
            cursor.execute("select airport.name from airport where airport.ident =%s", (row[0],))
            name = cursor.fetchone()
            if name:
                info = {"name": name[0], "ident": row[0]}
                listOfDicts.append(info)
        return jsonify(listOfDicts)
    except mysql.connector.Error as err:
        print("Virhe: " , err)
        return jsonify({"error": "Tietokantavirhe"}), 500
    finally:
        if cursor:
            cursor.close()
        if yhteys:
            yhteys.close()

@app.route("/game/select_flight", methods=['POST'])
def select_flight():
    destination = request.form['to']
    location = session.get('location')
    price = get_flight_price(location, destination)
    print(f"Price : {price}")

    #location = ICAO koodi kuten EFHK
    if price is not None:
        session['budget'] -= price
        session['round'] += 1
        session['location'] = destination
        print("Uusi sijainti:", session['location'])

    session['story'] = get_story()

    minigame= get_minigame_for_player()
    print("Valittu minipeli:", minigame)
    return minigame_select(minigame)


@app.route("/info", methods=['GET'])
def info():
    yhteys = get_connection()
    cursor = yhteys.cursor()
    location = session.get('location')
    cursor.execute("select country.name from country inner join airport on airport.iso_country = country.iso_country where ident = %s", (session['location'],))
    result = cursor.fetchone()

    return jsonify({"location": result[0], "budget": session['budget']})

@app.route('/game/get_story', methods = ['GET'])
def story_minigame():
    print("story_minigame activated")
    story = session.get('story', None)

    if story is not None:
        story_text = story
    elif story is None:
        story_text = ""

    print("tarina return: ", story)
    return jsonify({"story": story_text})

@app.route("/game/get_price", methods=['GET'])
def price_minigame():
    location = session.get('location')
    destination = request.args.get('ident1')
    price = get_flight_price(location, destination)

    if price is not None:
        return jsonify({"price": price})
    else:
        return jsonify({"error": "Hintaa ei löytynyt"}), 404
if __name__ == "__main__":
    app.run(debug=True)