# -*- coding: utf-8 -*-

import json
import os
import sys

import requests
from flask import Flask, redirect, render_template, request, session, url_for

from scripts import forms, helpers, mongodb, tabledef

app = Flask(__name__)
app.config["SECRET_KEY"] = "asteria"
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

API_URL = "https://placeholderapi.herokuapp.com"

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
                # Changed to Mongo
                if mongodb.credentials_valid(username, password):
                    session["logged_in"] = True
                    session["username"] = username
                    response = {"status": "Login successful"}
                    mongodb.log("login", request.remote_addr,
                                username, request.form, response, 200)
                    return json.dumps(response)
                response = {"status": "Invalid user/pass"}
                mongodb.log("login", request.remote_addr,
                            username, request.form, response, 400)
                return json.dumps(response)
            response = {"status": "Both fields required"}
            mongodb.log("login", request.remote_addr,
                        username, request.form, response, 400)
            return json.dumps(response)
        response = render_template("login.html", form=form)
        mongodb.log("visit", request.remote_addr, "-", "login.html", "-", 200)
        return response
    user = mongodb.get_user()   # Changed to Mongo
    mongodb.log("visit", request.remote_addr,
                user.username, "home.html", "-", 200)
    return render_template("home.html", user=user, users=requests.get(API_URL + "/api/v1.0/users").json()["Users"])


@app.route("/logout")
def logout():
    mongodb.log("logout", request.remote_addr,
                session['username'], "-", "-", 200)
    session["logged_in"] = False
    return redirect(url_for("login"))


# -------- Signup ---------------------------------------------------------- #
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if not session.get("logged_in"):
        form = forms.LoginForm(request.form)
        if request.method == "POST":
            username = request.form["username"].lower()
            password = mongodb.hash_password(
                request.form["password"])      # Changed to Mongo
            email = request.form["email"]
            if form.validate():
                # Changed to Mongo
                if not mongodb.username_taken(username):
                    # Changed to Mongo
                    mongodb.add_user(username, password, email)
                    session["logged_in"] = True
                    session["username"] = username
                    response = {"status": "Signup successful"}
                    mongodb.log("signup", request.remote_addr,
                                username, request.form, response, 200)
                    return json.dumps(response)
                response = {"status": "Username taken"}
                mongodb.log("signup", request.remote_addr,
                            username, request.form, response, 400)
                return json.dumps(response)
            response = {"status": "User/Pass required"}
            mongodb.log("signup", request.remote_addr,
                        username, request.form, response, 400)
            return json.dumps(response)
        response = render_template("login.html", form=form)
        mongodb.log("visit", request.remote_addr, "-", "login.html", "-", 200)
        return response
    mongodb.log("visit", request.remote_addr, "-", "login.html", "-", 200)
    return redirect(url_for("login"))


# -------- Settings ---------------------------------------------------------- #
@app.route("/settings", methods=["GET", "POST"])
def settings():
    if session.get("logged_in"):
        if request.method == "POST":
            password = request.form["password"]
            if password != "":
                password = mongodb.hash_password(
                    password)      # Changed to Mongo
            email = request.form["email"]
            # Changed to Mongo
            mongodb.change_user(password=password, email=email)
            response = {"status": "Saved"}
            mongodb.log("update", request.remote_addr,
                        session['username'], request.form, response, 200)
            return json.dumps(response)
        user = mongodb.get_user()                           # Changed to Mongo
        response = render_template("settings.html", user=user)
        mongodb.log("visit", request.remote_addr,
                    "-", "settings.html", "-", 200)
        return response
    mongodb.log("visit", request.remote_addr, "-", "login.html", "-", 200)
    return redirect(url_for("login"))

# -------- Pages ------------------------------------------------------------- #
@app.route("/start-experiment")
def start():
    return render_template('start_experiment.html')

@app.route("/my-experiments")
def experiments():
    return render_template('my_experiments.html')

@app.route("/my-account")
def account():
    return render_template('my_account.html')

# ======== Main ============================================================== #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(debug=True, use_reloader=True)
