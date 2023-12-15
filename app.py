import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
import requests
import jwt
import datetime
import hashlib

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

SECRET_KEY = "SKILLHUB"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/discover')
def discover():
    return render_template('discover.html')

@app.route("/register", methods=["GET"])
def register():
    return render_template("register.html")

@app.route("/api/register", methods=["POST"])
def api_register():
    id_receive = request.form["id_give"]

    existing_user = db.user.find_one({"id": id_receive})
    if existing_user:
        msg = f"An account with id {id_receive} already exists!"
        return jsonify({"result": "failure", "msg": msg})

    pw_receive = request.form["pw_give"]
    nickname_receive = request.form["nickname_give"]
    role_receive = request.form.get("role_give")


    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    db.user.insert_one({
        "id": id_receive, 
        "pw": pw_hash, 
        "nick": nickname_receive,
        "role": role_receive
    })

    return jsonify({"result": "success"})

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({
        "id": id_receive, 
        "pw": pw_hash
    }, {"role": 1, "_id": 0})


    if result is not None:
        user_role = result.get("role", None)

        payload = {
            "id": id_receive,
            "role": user_role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24),
        }

        if user_role == "admin":
            return jsonify({
                "result": "success", 
                "token": jwt.encode(payload, SECRET_KEY, algorithm="HS256"),
                "redirect": "/home_pemilik"
            })
        else:
            return jsonify({
                "result": "success", 
                "token": jwt.encode(payload, SECRET_KEY, algorithm="HS256"),
                "redirect": "/home_visitor"
            })
    else:
        return jsonify({
            "result": "fail", 
            "msg": "your username or password is incorrect"
        })

@app.route('/home_visitor')
def home_visitor():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        
        if payload["role"] == "admin":
            return redirect(url_for("home_pemilik"))
        
        return render_template("home_visitor.html")
    except jwt.ExpiredSignatureError:
        return redirect(url_for(
            "login", 
            msg="Your login token has expired"
            ))
    except jwt.exceptions.DecodeError:
        return redirect(url_for(
            "login", 
            msg="There was an issue logging you in"))
            
@app.route('/home_pemilik')
def home_pemilik():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])

        if payload["role"] != "admin":
            return redirect(url_for("home_visitor"))

        return render_template("home_pemilik.html")
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="Your login token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="There was an issue logging you in"))

@app.route('/cekpembayaran_visitor')
def cekpembayaran_visitor():
    return render_template('cekpembayaran_visitor.html')

@app.route('/cekpembayaran_pemilik')
def cekpembayaran_pemilik():
    return render_template('cekpembayaran_pemilik.html')

@app.route('/detailcourse_visitor')
def detailcourse_visitor():
    return render_template('detailcourse_visitor.html')

@app.route('/detailcourse_pemilik')
def detailcourse_pemilik():
    return render_template('detailcourse_pemilik.html')

@app.route('/discover_visitor')
def discover_visitor():
    return render_template('discover_visitor.html')

@app.route('/discover_pemilik')
def discover_pemilik():
    return render_template('discover_pemilik.html')

@app.route('/listcourse_visitor')
def listcourse_visitor():
    return render_template('listcourse_visitor.html')

@app.route('/listcourse_pemilik')
def listcourse_pemilik():
    return render_template('listcourse_pemilik.html')

@app.route('/mycourse_visitor')
def mycourse_visitor():
    return render_template('mycourse_visitor.html')

@app.route('/mycourse_pemilik')
def mycourse_pemilik():
    return render_template('mycourse_pemilik.html')

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)