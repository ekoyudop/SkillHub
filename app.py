import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, jsonify
from pymongo import MongoClient
import requests
import jwt
import datetime
import hashlib
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

SECRET_KEY = "SKILLHUB"

@app.route('/', methods = ['GET'])
def index():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_admin = user_info.get("role") == "admin"
        logged_in = True
        
        return render_template("index.html", user_info=user_info, is_admin = is_admin, logged_in = logged_in)
    
    except jwt.ExpiredSignatureError:
        return render_template("index.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("index.html", msg="There was problem logging you in")
    
@app.route('/register')
def register():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        
        return redirect(url_for("index"))
    
    except jwt.ExpiredSignatureError:
        return render_template("register.html")
    except jwt.exceptions.DecodeError:
        return render_template("register.html")
    
@app.route('/login')
def login():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        
        return redirect(url_for("index"))
    
    except jwt.ExpiredSignatureError:
        return render_template("login.html")
    except jwt.exceptions.DecodeError:
        return render_template("login.html")
    
@app.route('/discover', methods = ['GET'])
def discover():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_admin = user_info.get("role") == "admin"
        logged_in = True

        kategori_list = db.kategori.find()

        return render_template("discover.html", user_info=user_info, is_admin = is_admin, logged_in = logged_in, kategori_list=kategori_list)
    
    except jwt.ExpiredSignatureError:
        return render_template("discover.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("discover.html", msg="There was problem logging you in")
    
@app.route("/add_kategori", methods=["POST"])
def add_kategori():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])

        kategori_receive = request.form["kategori_give"]

        existing_kategori = db.kategori.find_one({"kategori": kategori_receive})
        if existing_kategori:
            return jsonify({"result": "error", "message": "Kategori sudah ada."})

        db.kategori.insert_one({
            "kategori": kategori_receive 
        })

        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("discover"))
    
@app.route('/edit_kategori/<string:kategori_id>', methods=['PUT'])
def edit_kategori(kategori_id):
    try:
        kategori_edit = request.form.get('kategori_edit')

        result = db.kategori.update_one({'_id': ObjectId(kategori_id)}, {'$set': {'kategori': kategori_edit}})
        
        if result.modified_count > 0:
            response = {'result': 'success', 'message': 'Kategori edited successfully.'}
        else:
            response = {'result': 'error', 'message': 'Kategori not found or no changes made.'}
    except Exception as e:
        response = {'result': 'error', 'message': str(e)}

    return jsonify(response)

    
@app.route('/delete_kategori/<string:kategori_id>', methods=['DELETE'])
def delete_kategori(kategori_id):
    try:
        result = db.kategori.delete_one({'_id': ObjectId(kategori_id)})
        if result.deleted_count > 0:
            response = {'result': 'success', 'message': 'Kategori deleted successfully.'}
        else:
            response = {'result': 'error', 'message': 'Kategori not found.'}
    except Exception as e:
        response = {'result': 'error', 'message': str(e)}

    return jsonify(response)

@app.route('/mycourse', methods = ['GET'])
def mycourse():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_admin = user_info.get("role") == "admin"
        logged_in = True
        
        return render_template("mycourse.html", user_info=user_info, is_admin = is_admin, logged_in = logged_in)
    
    except jwt.ExpiredSignatureError:
        return render_template("mycourse.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("mycourse.html", msg="There was problem logging you in")
    
@app.route('/cekpembayaran', methods = ['GET'])
def cekpembayaran():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_admin = user_info.get("role") == "admin"
        logged_in = True
        
        return render_template("cekpembayaran.html", user_info=user_info, is_admin = is_admin, logged_in = logged_in)
    
    except jwt.ExpiredSignatureError:
        return render_template("cekpembayaran.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("cekpembayaran.html", msg="There was problem logging you in")
    
@app.route('/listcourse', methods = ['GET'])
def listcourse():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_admin = user_info.get("role") == "admin"
        logged_in = True
        
        return render_template("listcourse.html", user_info=user_info, is_admin = is_admin, logged_in = logged_in)
    
    except jwt.ExpiredSignatureError:
        return render_template("listcourse.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("listcourse.html", msg="There was problem logging you in")
    
@app.route('/detailcourse', methods = ['GET'])
def detailcourse():
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_admin = user_info.get("role") == "admin"
        logged_in = True
        
        return render_template("detailcourse.html", user_info=user_info, is_admin = is_admin, logged_in = logged_in)
    
    except jwt.ExpiredSignatureError:
        return render_template("detailcourse.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("detailcourse.html", msg="There was problem logging you in")

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

@app.route("/api/login", methods=["POST"])
def api_login():
    id_receive = request.form["id_give"]
    pw_receive = request.form["pw_give"]

    pw_hash = hashlib.sha256(pw_receive.encode("utf-8")).hexdigest()

    result = db.user.find_one({
        "id": id_receive, 
        "pw": pw_hash
    }, {"role": 1})

    if result:
        user_role = result.get("role", None)

        payload = {
            "id": id_receive,
            "role": user_role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

        return jsonify(
            {
                "result": "success",
                "token": token,
            }
        )
    else:
        return jsonify({
            "result": "fail", 
            "msg": "your username or password is incorrect"
        })

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)