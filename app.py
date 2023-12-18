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
        if token_receive:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
            user_info = db.user.find_one({"id": payload["id"]})
            is_member = user_info.get("role") == "member"
            is_admin = user_info.get("role") == "admin"
            logged_in = True
        else:
            user_info = None
            is_admin = False
            logged_in = False
            is_member = False

        course_list = db.course.find()
        
        return render_template("index.html", user_info=user_info, is_member = is_member,is_admin = is_admin, logged_in = logged_in, course_list=course_list)
    
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
        if token_receive:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
            user_info = db.user.find_one({"id": payload["id"]})
            is_member = user_info.get("role") == "member"
            is_admin = user_info.get("role") == "admin"
            logged_in = True
        else:
            user_info = None
            is_admin = False
            logged_in = False
            is_member = False

        course_list = db.course.find()

        return render_template("discover.html", 
                               user_info=user_info, 
                               is_member = is_member,
                               is_admin = is_admin,
                               logged_in = logged_in,
                               course_list=course_list)
    
    except jwt.ExpiredSignatureError:
        return render_template("discover.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("discover.html", msg="There was problem logging you in")
    
@app.route('/discover/previewcourse/<string:course_id>', methods = ['GET'])
def previewcourse(course_id):
    token_receive = request.cookies.get("mytoken")
    try:
        if token_receive:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
            user_info = db.user.find_one({"id": payload["id"]})
            is_member = user_info.get("role") == "member"
            is_admin = user_info.get("role") == "admin"
            logged_in = True
        else:
            user_info = None
            is_admin = False
            logged_in = False
            is_member = False
        
        course_list = db.course.find_one({'_id': ObjectId(course_id)})

        return render_template("previewcourse.html", 
                               user_info=user_info, 
                               is_member = is_member,
                               is_admin = is_admin, 
                               logged_in = logged_in,
                               course_list=course_list)
    
    except jwt.ExpiredSignatureError:
        return render_template("previewcourse.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("previewcourse.html", msg="There was problem logging you in")

@app.route('/mycourse', methods = ['GET'])
def mycourse():
    token_receive = request.cookies.get("mytoken")
    try:
        if token_receive:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
            user_info = db.user.find_one({"id": payload["id"]})
            is_member = user_info.get("role") == "member"
            is_admin = user_info.get("role") == "admin"
            role = user_info.get("role")
            logged_in = True
        else:
            user_info = None
            is_admin = False
            logged_in = False

        course_list = db.course.find()

        if role not in ["admin", "member"]:
            return redirect(url_for("cekpembayaran", id=payload["id"]))
        
        return render_template("mycourse.html", 
                               user_info=user_info, 
                               is_member = is_member,
                               is_admin = is_admin, 
                               logged_in = logged_in, 
                               course_list = course_list)
    
    except jwt.ExpiredSignatureError:
        return render_template("mycourse.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("mycourse.html", msg="There was problem logging you in")

@app.route('/mycourse/detailcourse/<string:course_id>', methods = ['GET'])
def detailcourse(course_id):
    token_receive = request.cookies.get("mytoken")
    try:
        if token_receive:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
            user_info = db.user.find_one({"id": payload["id"]})
            is_member = user_info.get("role") == "member"
            is_admin = user_info.get("role") == "admin"
            role = user_info.get("role")
            logged_in = True
        else:
            user_info = None
            is_admin = False
            logged_in = False

        course_list = db.course.find_one({'_id': ObjectId(course_id)})

        if role not in ["admin", "member"]:
            return redirect(url_for("cekpembayaran", id=payload["id"]))

        return render_template("detailcourse.html", 
                               user_info=user_info, 
                               is_admin = is_admin, 
                               is_member = is_member,
                               logged_in = logged_in,
                               course_list = course_list)
    
    except jwt.ExpiredSignatureError:
        return render_template("detailcourse.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("detailcourse.html", msg="There was problem logging you in")
    
@app.route('/cekpembayaran/<id>', methods = ['GET'])
def cekpembayaran(id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(
            token_receive, 
            SECRET_KEY, 
            algorithms=["HS256"])
        user_info = db.user.find_one({"id": payload["id"]})
        is_member = user_info.get("role") == "member"
        is_admin = user_info.get("role") == "admin"
        logged_in = True

        pembayaran_info = db.pembayaran.find()
        
        return render_template("cekpembayaran.html", 
                               user_info=user_info, 
                               is_admin = is_admin, 
                               is_member = is_member,
                               logged_in = logged_in,
                               pembayaran_info=pembayaran_info)
    
    except jwt.ExpiredSignatureError:
        return render_template("cekpembayaran.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("cekpembayaran.html", msg="There was problem logging you in")
    
@app.route('/datapembayaran', methods = ['GET'])
def datapembayaran():
    token_receive = request.cookies.get("mytoken")
    try:
        if token_receive:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])
            user_info = db.user.find_one({"id": payload["id"]})
            is_admin = user_info.get("role") == "admin"
            logged_in = True
        else:
            user_info = None
            is_admin = False
            logged_in = False

        pembayaran_list = db.pembayaran.find()

        return render_template("datapembayaran.html", 
                               user_info=user_info, 
                               is_admin = is_admin,
                               logged_in = logged_in,
                               pembayaran_list = pembayaran_list)
    
    except jwt.ExpiredSignatureError:
        return render_template("datapembayaran.html", msg="Your token has expired")
    except jwt.exceptions.DecodeError:
        return render_template("datapembayaran.html", msg="There was problem logging you in")
    
@app.route("/accept_pembayaran/<string:pembayaran_id>", methods=["PUT"])
def accept_pembayaran(pembayaran_id):
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])

        role_receive = request.form["role_give"]
        status_receive = request.form["status_give"]
        user_receive = request.form["user_give"] 


        print("user_receive:", user_receive)

        db.pembayaran.update_one(
            {"_id": ObjectId(pembayaran_id)},
            {"$set": {"status": status_receive}}
        )

        db.user.update_one(
            {"id": user_receive},
            {"$set": {"role": role_receive}}
        )

        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))

@app.route("/pembayaran", methods=["POST"])
def pembayaran():
    from datetime import datetime
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])

        id_receive = request.form["id_give"]
        status_receive = request.form["status_give"]
        image_receive = request.files["image_give"]

        today = datetime.now()
        mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

        if image_receive:
            extension = image_receive.filename.split('.')[-1]
            filename = f'static/post-{mytime}.{extension}'
            image_receive.save(filename)

        db.pembayaran.insert_one({
            "user": id_receive,
            "status": status_receive,
            "image": filename if image_receive else None
        })

        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("index"))
    
@app.route("/add_course", methods=["POST"])
def add_course():
    from datetime import datetime
    token_receive = request.cookies.get("mytoken")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=["HS256"])

        course_receive = request.form["course_give"]
        deskripsi_receive = request.form["deskripsi_give"]
        linkembed_receive = request.form["linkembed_give"]
        judul1_receive = request.form["judul1_give"]
        materi1_receive = request.form["materi1_give"]
        judul2_receive = request.form["judul2_give"]
        materi2_receive = request.form["materi2_give"]
        judul3_receive = request.form["judul3_give"]
        materi3_receive = request.form["materi3_give"]
        judul4_receive = request.form["judul4_give"]
        materi4_receive = request.form["materi4_give"]
        judul5_receive = request.form["judul5_give"]
        materi5_receive = request.form["materi5_give"]
        image_receive = request.files["image_give"]

        today = datetime.now()
        mytime = today.strftime("%Y-%m-%d-%H-%M-%S")

        if image_receive:
            extension = image_receive.filename.split('.')[-1]
            filename = f'static/post-{mytime}.{extension}'
            image_receive.save(filename)


        existing_course = db.course.find_one({"course": course_receive})
        if existing_course:
            return jsonify({"result": "error", "message": "Course sudah ada."})

        db.course.insert_one({
            "course": course_receive,
            "deskripsi": deskripsi_receive,
            "linkembed": linkembed_receive,
            "judul1": judul1_receive,
            "materi1": materi1_receive,
            "judul2": judul2_receive,
            "materi2": materi2_receive,
            "judul3": judul3_receive,
            "materi3": materi3_receive,
            "judul4": judul4_receive,
            "materi4": materi4_receive,
            "judul5": judul5_receive,
            "materi5": materi5_receive,
            "image": filename if image_receive else None
        })

        return jsonify({"result": "success"})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("discover"))
         
@app.route('/delete_course/<string:course_id>', methods=['DELETE'])
def delete_course(course_id):
    try:
        result = db.course.delete_one({'_id': ObjectId(course_id)})
        if result.deleted_count > 0:
            response = {'result': 'success', 'message': 'course deleted successfully.'}
        else:
            response = {'result': 'error', 'message': 'Course not found.'}
    except Exception as e:
        response = {'result': 'error', 'message': str(e)}

    return jsonify(response)

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