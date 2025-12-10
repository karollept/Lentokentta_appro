# app.py
from flask import Flask, request, jsonify, make_response, session
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "lk_approt",
    "autocommit": False
}

ALLOWED_COUNTRIES = [
    "FI", "SE", "DK", "EE", "NL", "AD", "TR", "GR",
    "AZ", "RS", "DE", "SK", "CH", "BE", "HU",
    "RO", "MD", "IE", "AM", "UA", "PT", "SI",
    "GB", "LU", "ES", "BY", "RU", "CY",
    "NO", "CZ", "FR", "ME", "XK", "IS", "LV", "IT",
    "BA", "MK", "BG", "GE", "AL",
    "MT", "PL", "LT", "AT", "HR"
]

app = Flask(__name__)
app.secret_key = "meow"
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def query_db(query, params=None, fetchone=False, fetchall=False, commit=False):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        result = None
        if fetchone:
            result = cursor.fetchone()
        elif fetchall:
            result = cursor.fetchall()
        if commit:
            conn.commit()
        return result
    except Error as e:
        if conn:
            conn.rollback()
        print("[DB ERROR]", e)
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "OK", "message": "Lentokenttä Approt API toimii!"})


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("name")
    age = data.get("age")
    password = data.get("password")

    if not username or age is None or not password:
        return jsonify({"error": "Täytä kaikki kentät"}), 400

    existing = query_db("SELECT user_id FROM users WHERE username = %s", (username,), fetchone=True)
    if existing:
        return jsonify({"error": "Käyttäjänimi on jo olemassa"}), 400

    hashed = generate_password_hash(password)
    query_db(
        "INSERT INTO users (username, age, password, signup_timestamp) VALUES (%s, %s, %s, NOW())",
        (username, int(age), hashed),
        commit=True
    )

    try:
        user = query_db("SELECT user_id FROM users WHERE username=%s", (username,), fetchone=True)

        query_db("""
            INSERT INTO player (user_id, screen_name, location, budget)
            VALUES (%s, %s, %s, %s)
        """, (user["user_id"], username, None, 0), commit=True)
    except Exception:
        pass

    return jsonify({"message": "Tili luotu onnistuneesti!"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("name")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Täytä kaikki kentät"}), 400

    user = query_db("SELECT * FROM users WHERE username = %s", (username,), fetchone=True)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Väärä käyttäjänimi tai salasana"}), 401

    query_db("UPDATE users SET last_login = %s WHERE user_id = %s", (datetime.now(), user["user_id"]), commit=True)

    try:
        query_db(
            "INSERT INTO sessions (user_id, screen_name, start_time) VALUES (%s, %s, NOW())",
            (user["user_id"], user["username"]),
            commit=True
        )
        last = query_db(
            "SELECT session_id FROM sessions WHERE user_id = %s ORDER BY start_time DESC LIMIT 1",
            (user["user_id"],),
            fetchone=True
        )
        session_id = last["session_id"] if last and "session_id" in last else None
    except Exception as e:
        print("[create session error]", e)
        session_id = None

    session["user_id"] = user["user_id"]
    session["username"] = user["username"]
    if session_id:
        session["session_id"] = session_id

    return jsonify({
        "message": "Kirjautuminen onnistui",
        "user_id": user["user_id"],
        "username": user["username"],
        "session_id": session_id
    })


@app.route("/logout", methods=["POST"])
def logout():
    sid = session.get("session_id")
    uid = session.get("user_id")
    try:
        if sid:
            query_db("UPDATE sessions SET end_time = NOW() WHERE session_id = %s", (sid,), commit=True)
        else:
            if uid:
                query_db("UPDATE sessions SET end_time = NOW() WHERE user_id = %s AND end_time IS NULL", (uid,), commit=True)
    except Exception as e:
        print("[logout error]", e)

    session.clear()
    return jsonify({"message": "Logged out"})


@app.route("/admin-login", methods=["POST"])
def admin_login():
    data = request.get_json() or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Täytä kaikki kentät"}), 400

    admin = query_db("SELECT * FROM admins WHERE username = %s", (username,), fetchone=True)
    if admin and check_password_hash(admin["password"], password):
        return jsonify({"message": "Admin kirjautuminen onnistui"})
    if username == "admin" and password == "admin":
        return jsonify({"message": "Admin kirjautuminen onnistui"})
    return jsonify({"error": "Virheellinen admin-tunnus tai salasana"}), 401


@app.route("/admin/stats", methods=["GET"])
def admin_stats():
    try:
        users_count = query_db("SELECT COUNT(*) AS cnt FROM users", fetchone=True)["cnt"]
        games_count = query_db("SELECT COUNT(*) AS cnt FROM minigame", fetchone=True)["cnt"]
        airports_count = query_db("SELECT COUNT(DISTINCT lentokentta) AS cnt FROM game_data", fetchone=True)["cnt"]
        countries_count = query_db("SELECT COUNT(DISTINCT valtio) AS cnt FROM game_data", fetchone=True)["cnt"]
        return jsonify({
            "users": int(users_count or 0),
            "games": int(games_count or 0),
            "airports": int(airports_count or 0),
            "countries": int(countries_count or 0)
        })
    except Exception as e:
        print("[stats error]", e)
        return jsonify({"error": "Cannot fetch stats"}), 500


@app.route("/admin/users", methods=["GET"])
def admin_users():
    try:
        rows = query_db("""
            SELECT u.user_id AS id, u.username, u.age,
                   u.signup_timestamp AS created_at, u.last_login,
                   p.budget AS budget, p.location AS current_airport
            FROM users u
            LEFT JOIN player p ON p.screen_name = u.username
            ORDER BY u.user_id DESC
        """, fetchall=True)
        for r in rows or []:
            r["budget"] = float(r["budget"]) if r.get("budget") is not None else 0
            if r.get("created_at"): r["created_at"] = r["created_at"].isoformat(sep=' ')
            if r.get("last_login"): r["last_login"] = r["last_login"].isoformat(sep=' ')
            if r.get("current_airport") is None:
                r["current_airport"] = '-'
            r["haalarimerkit"] = []
        return jsonify(rows or [])
    except Exception as e:
        print("[admin_users error]", e)
        return jsonify({"error": "Ei voitu ladata käyttäjiä"}), 500


@app.route("/admin/add_user", methods=["POST"])
def admin_add_user():
    data = request.get_json() or {}
    username = data.get("username") or data.get("name") or data.get("user")
    password = data.get("password")
    age = data.get("age")
    budget = data.get("budget", 0)

    if not username or not password:
        return jsonify({"error": "Täytä käyttäjänimi ja salasana"}), 400

    existing = query_db("SELECT user_id FROM users WHERE username = %s", (username,), fetchone=True)
    if existing:
        return jsonify({"error": "Käyttäjänimi on jo olemassa"}), 400

    hashed = generate_password_hash(password)
    try:
        query_db("INSERT INTO users (username, age, password, signup_timestamp) VALUES (%s, %s, %s, NOW())",
                 (username, age if age is not None else 0, hashed), commit=True)
        try:
            query_db("INSERT INTO player (screen_name, location, budget) VALUES (%s, %s, %s)",
                     (username, None, budget or 0), commit=True)
        except Exception:
            try:
                query_db("UPDATE player SET budget=%s WHERE screen_name=%s", (budget or 0, username), commit=True)
            except Exception:
                pass
        return jsonify({"message": "Käyttäjä luotu"}), 201
    except Exception as e:
        print("[add_user error]", e)
        return jsonify({"error": "Käyttäjän luomisessa tapahtui virhe"}), 500


@app.route("/admin/user/<int:user_id>", methods=["GET", "PUT", "DELETE"])
def admin_user(user_id):
    if request.method == "GET":
        user = query_db("""
            SELECT u.user_id AS id, u.username, u.age, u.signup_timestamp AS created_at, u.last_login,
                   p.budget AS budget, p.location AS current_airport
            FROM users u
            LEFT JOIN player p ON p.screen_name = u.username
            WHERE u.user_id = %s
        """, (user_id,), fetchone=True)
        if not user:
            return jsonify({"error": "Pelaajaa ei löytynyt"}), 404
        if user.get("created_at"): user["created_at"] = user["created_at"].isoformat(sep=' ')
        if user.get("last_login"): user["last_login"] = user["last_login"].isoformat(sep=' ')
        user["budget"] = float(user["budget"]) if user.get("budget") is not None else 0
        user["haalarimerkit"] = []
        return jsonify(user)

    if request.method == "PUT":
        data = request.get_json() or {}
        username = data.get("username")
        if not username:
            return jsonify({"error": "Ei päivitettäviä kenttiä"}), 400
        try:
            old = query_db("SELECT username FROM users WHERE user_id = %s", (user_id,), fetchone=True)
            if not old:
                return jsonify({"error": "Käyttäjää ei löydy"}), 404
            old_name = old["username"]
            query_db("UPDATE users SET username = %s WHERE user_id = %s", (username, user_id), commit=True)
            query_db("UPDATE player SET screen_name = %s WHERE screen_name = %s", (username, old_name), commit=True)
            return jsonify({"message": "Käyttäjätiedot päivitetty"})
        except Exception as e:
            print("[update user error]", e)
            return jsonify({"error": "Päivitys epäonnistui"}), 500

    if request.method == "DELETE":
        try:
            u = query_db("SELECT username FROM users WHERE user_id = %s", (user_id,), fetchone=True)
            if not u:
                return jsonify({"error": "Käyttäjää ei löydy"}), 404
            username = u["username"]
            query_db("DELETE FROM player WHERE screen_name = %s", (username,), commit=True)
            query_db("DELETE FROM sessions WHERE user_id = %s", (user_id,), commit=True)
            query_db("DELETE FROM game_logs WHERE user_id = %s", (user_id,), commit=True)
            query_db("DELETE FROM users WHERE user_id = %s", (user_id,), commit=True)
            return jsonify({"message": "Käyttäjä poistettu"})
        except Exception as e:
            print("[delete user error]", e)
            return jsonify({"error": "Poisto epäonnistui"}), 500


@app.route("/admin/update_password/<int:user_id>", methods=["POST"])
def admin_update_password(user_id):
    data = request.get_json() or {}
    newpw = data.get("password")
    if not newpw:
        return jsonify({"error": "Uusi salasana puuttuu"}), 400
    hashed = generate_password_hash(newpw)
    try:
        query_db("UPDATE users SET password = %s WHERE user_id = %s", (hashed, user_id), commit=True)
        return jsonify({"message": "Salasana päivitetty"})
    except Exception as e:
        print("[update_password error]", e)
        return jsonify({"error": "Ei voitu päivittää salasanaa"}), 500


@app.route("/admin/user/<int:user_id>/age", methods=["PUT"])
def admin_update_age(user_id):
    data = request.get_json() or {}
    age = data.get("age")
    if age is None:
        return jsonify({"error": "Ikä puuttuu"}), 400
    try:
        query_db("UPDATE users SET age = %s WHERE user_id = %s", (int(age), user_id), commit=True)
        return jsonify({"message": "Ikä päivitetty"})
    except Exception as e:
        print("[update_age error]", e)
        return jsonify({"error": "Ei voitu päivittää ikää"}), 500


@app.route("/admin/user/<int:user_id>/budget", methods=["PUT"])
def admin_update_budget(user_id):
    data = request.get_json() or {}
    budget = data.get("budget")
    if budget is None:
        return jsonify({"error": "Budjetti puuttuu"}), 400
    try:
        user = query_db("SELECT username FROM users WHERE user_id = %s", (user_id,), fetchone=True)
        if not user:
            return jsonify({"error": "Käyttäjää ei löytynyt"}), 404
        username = user["username"]
        player = query_db("SELECT * FROM player WHERE screen_name = %s", (username,), fetchone=True)
        if player:
            query_db("UPDATE player SET budget = %s WHERE screen_name = %s", (float(budget), username), commit=True)
        else:
            query_db("INSERT INTO player (screen_name, location, budget) VALUES (%s, %s, %s)",
                     (username, "Unknown", float(budget)), commit=True)
        return jsonify({"message": "Budjetti päivitetty"})
    except Exception as e:
        print("[update_budget error]", e)
        return jsonify({"error": "Ei voitu päivittää budjettia"}), 500


@app.route("/admin/user/<int:user_id>/sessions", methods=["GET"])
def admin_list_sessions(user_id):
    try:
        rows = query_db(
            "SELECT session_id AS id, user_id, screen_name, start_time, end_time FROM sessions WHERE user_id = %s",
            (user_id,),
            fetchall=True
        )

        for r in rows or []:
            r["start_time"] = r["start_time"].isoformat(sep=' ') if r.get("start_time") else None
            r["end_time"]   = r["end_time"].isoformat(sep=' ') if r.get("end_time") else None

        return jsonify(rows or [])
    except Exception as e:
        print("[list_sessions error]", e)
        return jsonify({"error": "Ei voitu hakea sessioita"}), 500


@app.route("/admin/session/<int:session_id>", methods=["DELETE"])
def admin_delete_session(session_id):
    try:
        query_db("DELETE FROM sessions WHERE session_id = %s", (session_id,), commit=True)
        query_db("DELETE FROM game_logs WHERE session_id = %s", (session_id,), commit=True)
        return jsonify({"message": "Sessio poistettu"})
    except Exception as e:
        print("[delete_session error]", e)
        return jsonify({"error": "Ei voitu poistaa sessiota"}), 500


@app.route("/admin/user/<int:user_id>/sessions", methods=["DELETE"])
def admin_user_sessions_delete(user_id):
    return jsonify({"error": "Not implemented"}), 405


@app.route("/current-user", methods=["GET"])
def current_user():
    """Return the current logged-in user details from the Flask session."""
    if "user_id" not in session:
        return jsonify({"logged_in": False}), 200
    return jsonify({
        "logged_in": True,
        "user_id": session.get("user_id"),
        "username": session.get("username"),
        "session_id": session.get("session_id")
    })

@app.route("/admin/game_data", methods=["GET"])
def admin_game_data():
    """
    Returns game data for admin UI. Uses ALLOWED_COUNTRIES (Finnish names).
    If you later want to expand to all countries, remove the c.name IN (...) filter.
    """
    try:
        placeholders = ",".join(["%s"] * len(ALLOWED_COUNTRIES))

        query = f"""
            SELECT
                c.name AS valtio,
                c.iso_country AS maatunnus,
                a.name AS lentokentta,
                a.ident AS ident,
                t.name AS token,
                '' AS haalarimerkin_nimi,
                s.story AS tarinat,
                m.name AS minipeli,
                -- aggregate connections so each airport appears only once
                GROUP_CONCAT(DISTINCT con.ident2 SEPARATOR ',') AS yhteysmaat,
                GROUP_CONCAT(DISTINCT con.price SEPARATOR ',') AS yhteyshinnat
            FROM airport a
            LEFT JOIN country c ON a.iso_country = c.iso_country
            LEFT JOIN stories s ON s.ident = a.ident
            LEFT JOIN minigame m ON m.ID = a.minigame_id
            LEFT JOIN token t ON t.ID = a.token_id
            LEFT JOIN connection con ON con.ident1 = a.ident
            WHERE a.iso_country IN ({placeholders})
              AND (
                    s.id IS NOT NULL
                    OR a.minigame_id IS NOT NULL
                    OR a.token_id IS NOT NULL
                    OR con.id IS NOT NULL
                  )
            GROUP BY a.ident, c.name, c.iso_country, a.name, t.name, s.story, m.name
            ORDER BY c.name ASC, a.name ASC;
        """

        rows = query_db(query, ALLOWED_COUNTRIES, fetchall=True)
        return jsonify(rows or [])
    except Exception as e:
        print("[REAL_GAME_DATA error]", e)
        return jsonify({"error": "Ei voitu ladata pelidataa"}), 500

@app.route("/admin/connections/<ident>", methods=["GET"])
def admin_connections(ident):
    """
    Returns connections for an airport ident.
    Fields:
      - ident2 (destination airport ident)
      - country_name (friendly name)
      - price
    """
    try:
        rows = query_db("""
            SELECT DISTINCT
                con.ident2 AS ident2,
                COALESCE(c.name, a2.name, a2.iso_country, '') AS country_name,
                con.price AS price
            FROM connection con
            LEFT JOIN airport a1 ON a1.ident = con.ident1
            LEFT JOIN airport a2 ON a2.ident = con.ident2
            LEFT JOIN country c ON c.iso_country = a2.iso_country
            WHERE con.ident1 = %s
            ORDER BY con.price ASC
            LIMIT 50
        """, (ident,), fetchall=True)

        for r in (rows or []):
            r.setdefault('ident2', '')
            r.setdefault('country_name', '')
            r.setdefault('price', 0)

        return jsonify(rows or [])
    except Exception as e:
        print("[admin_connections error]", e)
        return jsonify({"error": "Ei voitu hakea yhteyksiä"}), 500


@app.route("/api/connections", methods=["GET"])
def api_connections():
    ident = request.args.get("ident")
    if not ident:
        return jsonify([])

    try:
        rows = query_db("""
            SELECT DISTINCT con.ident2 AS destination,
                   COALESCE(c.name, a2.name, a2.iso_country, '') AS country_name,
                   con.price AS price
            FROM connection con
            LEFT JOIN airport a2 ON a2.ident = con.ident2
            LEFT JOIN country c ON c.iso_country = a2.iso_country
            WHERE con.ident1 = %s
            ORDER BY con.price ASC
            LIMIT 50
        """, (ident,), fetchall=True)
        for r in (rows or []):
            r.setdefault('destination', '')
            r.setdefault('country_name', '')
            r.setdefault('price', 0)
        return jsonify(rows or [])
    except Exception as e:
        print("[api_connections error]", e)
        return jsonify([]), 500


@app.route("/player/<int:user_id>", methods=["GET"])
def player_data(user_id):
    p = query_db("SELECT * FROM player WHERE ID = %s", (user_id,), fetchone=True)
    if not p:
        return jsonify({"error": "Pelaajaa ei löytynyt"}), 404
    return jsonify(p)


@app.route("/logs/<int:user_id>", methods=["GET"])
def user_logs(user_id):
    logs = query_db("SELECT * FROM game_logs WHERE user_id = %s ORDER BY timestamp DESC", (user_id,), fetchall=True)
    return jsonify(logs or [])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

