# -*- coding: utf-8 -*-

import json
import os
import sys

from flask import Flask, redirect, render_template, request, session, url_for

from scripts import forms, helpers, tabledef
from scripts import mongodb


app = Flask(__name__)
app.config["SECRET_KEY"] = "asteria"

API_URL = "http://localhost:5001"

# Heroku
# from flask_heroku import Heroku
# heroku = Heroku(app)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route("/", methods=["GET", "POST"])
def login():
    if not session.get("logged_in"):
        form = forms.LoginForm(request.form)
        if request.method == "POST":
            username = request.form["username"].lower()
            password = request.form["password"]
            if form.validate():
                if mongodb.credentials_valid(username, password):   # Changed to Mongo
                    session["logged_in"] = True
                    session["username"] = username
                    return json.dumps({"status": "Login successful"})
                return json.dumps({"status": "Invalid user/pass"})
            return json.dumps({"status": "Both fields required"})
        return render_template("login.html", form=form)
    user = mongodb.get_user()   # Changed to Mongo
    return render_template("home.html", user=user)


@app.route("/logout")
def logout():
    session["logged_in"] = False
    return redirect(url_for("login"))


# -------- Signup ---------------------------------------------------------- #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if not session.get("logged_in"):
        form = forms.LoginForm(request.form)
        if request.method == "POST":
            username = request.form["username"].lower()
            password = mongodb.hash_password(request.form["password"])      # Changed to Mongo
            email = request.form["email"]
            if form.validate():
                if not mongodb.username_taken(username):            # Changed to Mongo  
                    mongodb.add_user(username, password, email)     # Changed to Mongo
                    session["logged_in"] = True 
                    session["username"] = username
                    return json.dumps({"status": "Signup successful"})
                return json.dumps({"status": "Username taken"})
            return json.dumps({"status": "User/Pass required"})
        return render_template("login.html", form=form)
    return redirect(url_for("login"))


# -------- Settings ---------------------------------------------------------- #
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if session.get("logged_in"):
        if request.method == "POST":
            password = request.form["password"]
            if password != "":
                password = mongodb.hash_password(password)      # Changed to Mongo
            email = request.form["email"]
            mongodb.change_user(password=password, email=email)     # Changed to Mongo
            return json.dumps({"status": "Saved"})
        user = mongodb.get_user()                           # Changed to Mongo
        return render_template("settings.html", user=user)
    return redirect(url_for("login"))


# ======== Main ============================================================== #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(debug=True, use_reloader=True)
