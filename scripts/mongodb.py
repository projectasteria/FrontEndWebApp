import datetime
import json
import os

import bcrypt
from flask import session
from pymongo import MongoClient

if "credentials.json" not in os.listdir('.'):
    data = {"mongo_URI" : os.environ['mongo_URI']}

else:
    data = json.load(open("credentials.json", "r"))

MONGO_CLIENT = MongoClient(data["mongo_URI"])

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.password = password
        self. email = email
    def __repr__(self):
        return '<User %r>' % self.username

def add_user(username, password, email):
    client = MONGO_CLIENT
    collection = client.asteria.usercred
    entry = {"username": username.lower(), "password":password, "email":email.lower(), "time_of_creation":datetime.datetime.utcnow()}
    collection.insert_one(entry)
    client.close()
    return True

def log(action, ip, username, incoming, outgoing, status):
    client = MONGO_CLIENT
    collection = client.asteria.logs
    entry = {"username":username.lower(), "action":action, "ip": ip, "incoming": incoming, "outgoing":outgoing, "status":status, "timestamp": datetime.datetime.utcnow()}
    collection.insert_one(entry)
    client.close()
    return True

def credentials_valid(username, password):
    client = MONGO_CLIENT
    collection = client.asteria.usercred
    res = collection.find_one({"username":username.lower()})
    client.close()
    if res != None:
        return bcrypt.checkpw(password.encode(), res["password"])
    return False

def username_taken(username):
    client = MONGO_CLIENT
    collection = client.asteria.usercred
    res = collection.find_one({"username":username.lower()})
    client.close()
    if res != None:
        return True
    return False

def get_user():
    username = session['username']
    client = MONGO_CLIENT
    collection = client.asteria.usercred
    res = collection.find_one({"username":username.lower()})
    client.close()
    return User(res['username'], res['email'], res['password'])

def hash_password(password):
    passwd = password.encode()
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed

def change_user(password, email):
    username = session['username']
    client = MONGO_CLIENT
    collection = client.asteria.usercred
    collection.update_one({'username':username.lower()}, {"$set":{"password": password, "email": email}})
