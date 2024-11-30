import sys
sys.path.append(".")
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_wtf.csrf import CSRFProtect
from libs import database
from libs import generate_keys
import time

csrf_tok = generate_keys.generate_random_key(1024)

app = Flask(__name__)  # Исправлено имя на __name__
app.secret_key = csrf_tok
csrf = CSRFProtect(app)

def check_cookies(IP):
    """Функция для проверки куков и получения данных из базы."""
    cookie_data = database.get_data("database.db", "SELECT cookie_id, csrf FROM Cookie WHERE own_ip = ?", (IP,))

    if cookie_data:
        cookie_id, csrf_token = cookie_data
        cookie_session = request.cookies.get('session_id')
        cookie_csrf = request.cookies.get("csrf")

        # Проверяем идентификатор сессии и CSRF токен
        if cookie_id == cookie_session and csrf_token == cookie_csrf:
            return True
    return False

@app.route("/login")
def login():
    IP = request.remote_addr

    if check_cookies(IP):
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    IP = request.remote_addr

    if check_cookies(IP):
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/")
def redirecto():
    IP = request.remote_addr

    if check_cookies(IP):
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))


@app.route("/login/api", methods=['POST'])
def login_api():
    data = request.get_json()

    if data["type"] == "ident":
        username = data["username"]
        status = database.check_data("database.db", "SELECT Username FROM Users WHERE Username = ?", (username,))
        if status:
            return jsonify({"type" : "ident", "status" : "Finded"}), 200
    elif data["type"] == "auth":
        username = data["username"]
        passwd = data["passwd"]

        passwd_database = database.get_data("database.db", "SELECT Passwd FROM Users WHERE Username = ?", (username,))

        if passwd_database == passwd:
            resp = make_response("Кука установлена!")
            resp.set_cookie('session_id', username, max_age=60*60, secure=True, samesite='Lax')
            resp.set_cookie('own_ip', str(request.remote_addr), max_age=60*60, secure=True, samesite='Lax')
            resp.set_cookie('csrf', csrf_tok, max_age=60*60, secure=True, samesite='Lax')
            return jsonify({"type" : "auth", "status" : "passwd_valid", "csrf": csrf_tok}), 200
        else:
            return jsonify({"type" : "error", "message" : "Инвалид пароль"}), 401

    return jsonify({"type": "error", "message": "Invalid credentials."}), 401

if __name__ == "__main__":  # Исправлено имя на "__main__"
    app.run(host="0.0.0.0", port=5000, debug=True)  # Запуск приложения
