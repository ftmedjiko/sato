from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect('sato.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  pseudo TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return jsonify({"message": "SATO API est en ligne!", "status": "OK"})

@app.route('/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    pseudo = data.get('pseudo', 'TesteurBenin')
    print(f"Inscription recue: {email}")

    if not email or not password:
        return jsonify({"success": False, "message": "Email et mot de passe requis"}), 400

    try:
        conn = sqlite3.connect('sato.db')
        conn.execute("INSERT INTO users (email, password, pseudo) VALUES (?,?,?)",
                     (email, password, pseudo))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Utilisateur cree!", "user": {"email": email, "pseudo": pseudo}}), 200
    except:
        return jsonify({"success": False, "message": "Email deja utilise"}), 400

@app.route('/v1/users', methods=['GET'])
def list_users():
    conn = sqlite3.connect('sato.db')
    cur = conn.cursor()
    cur.execute("SELECT email, pseudo FROM users")
    users = [{"email": row[0], "pseudo": row[1]} for row in cur.fetchall()]
    conn.close()
    return jsonify({"count": len(users), "users": users})

if __name__ == '__main__':
    print("SATO tourne sur http://localhost:3000")
    print("Base de donnees: sato.db")
    app.run(host='0.0.0.0', port=3000, debug=True)