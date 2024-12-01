import sys
sys.path.append(".")
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from libs import database
from libs.timer import start_timer
import random

app = Flask(__name__)

def check_cookies(IP, session_id, own_ip):
    """Функция для проверки куков и получения данных из базы."""

    db_ip = database.get_data("database.db", "SELECT own_ip FROM Cookie WHERE own_ip = ?", (IP,))
    
    if db_ip != None:
        if db_ip == own_ip:
            session_id_db = database.get_data("database.db", "SELECT cookie_id FROM Cookie WHERE own_ip = ?", (own_ip,))
            if session_id_db == session_id:
                return True
            else:
                return False
        else:
            return False
    else:
        return False
    



@app.route("/login")
def login():
    IP = request.remote_addr
    
    session_id = request.cookies.get("session_id")
    own_ip = request.cookies.get("own_ip")
    
    if check_cookies(IP, session_id, own_ip):
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    IP = request.remote_addr
    session_id = request.cookies.get("session_id")
    own_ip = request.cookies.get("own_ip")
    
    if check_cookies(IP, session_id, own_ip):
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/")
def redirecto():
    IP = request.remote_addr
    session_id = request.cookies.get("session_id")
    own_ip = request.cookies.get("own_ip")
    
    if check_cookies(IP, session_id, own_ip):
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))
    
@app.route("/login/api", methods=['POST'])
def login_api():
    package = request.get_json()

    if package["type"] == "ident":
        user = package["username"]
        db_user = database.get_data("database.db", "SELECT Username FROM Users WHERE Username = ?", (user,))

        if db_user == user:  # Убедитесь, что db_user содержит нужное значение
            return jsonify({"type": "ident", "status": "finded"}), 200
        else:
            return jsonify({"type": "ident", "status": "not_finded"}), 200

    elif package["type"] == "auth":
        user = package["username"]
        passwd = package["password"]

        db_pass = database.get_data("database.db", "SELECT Passwd FROM Users WHERE Username = ?", (user,))

        if db_pass == passwd:

            resp = make_response(jsonify({"type": "auth", "status": "pass_valid"}), 200)
            
            session_id = str(random.randint(1, 99999999))
                
            resp.set_cookie("session_id", session_id, max_age=3600, secure=True, httponly=True)
            resp.set_cookie("username", user, max_age=3600, secure=True, httponly=False)
            resp.set_cookie("own_ip", request.remote_addr, max_age=3600, secure=True, httponly=True)
                
            database.execute_SQL("database.db", "INSERT INTO Cookie (cookie_id, own_ip) VALUES (?, ?)", (session_id, request.remote_addr))
            
            start_timer("cookie", request.remote_addr, 3600)
            
            return resp
        else:
            return jsonify({"type": "auth", "status": "pass_invalid"}), 200            
    else:
        return jsonify({"type": "error", "message": "invalid_request"}), 400


# @app.route("/dashboard/api")
# def dashoard_api():
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("static/https/certificate.crt", "static/https/private.key"))
