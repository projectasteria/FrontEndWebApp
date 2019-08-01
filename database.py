import pymongo
from flask import session 

#myclient = pymongo.MongoClient("mongodb://3.19.62.182:27017")
#mydb = myclient["project"]

def add_user(username, password, email):
    data = {"user_name": username, "password":password, "email": email.lower()}
    mycol = mydb["customers"]
    x = mycol.insert_one(data)
    print (x.inserted_id)
    print (x)

def validate_password(username, password):
    return True

def email_check(email):
    mycol = mydb["customers"]
    q = {"email": email.lower()}
    mydoc = mycol.find(q)
    result = (list(mydoc))
    if len(result) == 0:
        return True
    else:
        return False



def user_check(username):
    mycol = mydb["customers"]
    q = {"user_name": username}
    mydoc = mycol.find(q)
    result = (list(mydoc))
    if len(result) == 0:
        return True
    else:
        return False

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

def get_user():
    username = session['username']
    mycol = mydb["customers"]
    q = {"user_name": username}
    mydoc = mycol.find(q)
    result = (list(mydoc))[0]
    return User(result["user_name"], result["email"], result["password"])

def update_password(username, new_password):
    username = session['username']
    mycol = mydb["customers"]

    myquery = { "user_name": username }
    newvalues = { "$set": { "password": new_password} }

    mycol.update_one(myquery, newvalues)
