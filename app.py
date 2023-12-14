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

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home_visitor')
def home_visitor():
    return render_template('home_visitor.html')

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)