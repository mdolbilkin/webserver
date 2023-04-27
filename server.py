import flask
from flask import Flask, request
import time
import sqlite3

app = Flask(__name__)
db = []



@app.route("/status")
def hello():
    return "Hello"


@app.route("/send", methods=["POST"])
def send():
    data = request.json
    if not isinstance(data, dict):
        return flask.abort(400)
    if set(data.keys()) != {'name', 'readme'}:
        return flask.abort(400)
    if 'name' not in data or 'readme' not in data:
        return flask.abort(400)
    name = data['name']
    text = data['readme']
    if not isinstance(name, str) or not isinstance(text, str) or name == "" or text == "":
        return flask.abort(400)
    message = {
        'time': time.time(),
        'name': name,
        'readme': text,
    }
    db.append(message)
    return {'ok': True}


@app.route("/messages")
def get():
    try:
        after = float(request.args['after'])
    except:
        return flask.abort(400)
    result = []
    for message in db:
        if message['time'] > after:
            result.append(message)
            if len(result) >= 100:
                break
    return {'messages': result}


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    if not isinstance(data, dict):
        return flask.abort(400)
    if set(data.keys()) != {'login', 'pass'}:
        return flask.abort(400)
    if 'login' not in data or 'pass' not in data:
        return flask.abort(400)
    login = data['login']
    password = data['pass']
    if not isinstance(login, str) or not isinstance(password, str) or login == "" or password == "":
        return flask.abort(400)
    user = {
        'login': login,
        'pass': password
    }
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()
    user1 = (user['login'], user['pass'])
    cur.execute("INSERT INTO users VALUES(?, ?);", user1)
    con.commit()
    return {"ok": True}


@app.route("/login", methods=['POST'])
def logining():
    data = request.json
    if not isinstance(data, dict):
        return flask.abort(400)
    if set(data.keys()) != {'login', 'pass'}:
        return flask.abort(400)
    if 'login' not in data or 'pass' not in data:
        return flask.abort(400)
    login = data['login']
    password = data['pass']
    if not isinstance(login, str) or not isinstance(password, str) or login == "" or password == "":
        return flask.abort(400)
    con = sqlite3.connect("data.sqlite")
    cur = con.cursor()
    cur.execute("SELECT * FROM users;")
    all_results = cur.fetchall()
    for i in all_results:
        if i[0] == login and i[1] == password:
            return {'ok' : True}
    print(all_results)
    return {"ok" : False}


app.run()
