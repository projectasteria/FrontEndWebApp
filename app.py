#!/usr/bin/env python3

from scripts import tabledef
from scripts import forms
from scripts import helpers
from flask import Flask, redirect, url_for, render_template, request, session
import json
import sys
import os
import requests
from database import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lablam.2017'
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']='6LfZHqAUAAAAAFGzv6sjoJmxFbbzt1o9w7U64_MI'
app.config['RECAPTCHA_PRIVATE_KEY']='6LfZHqAUAAAAAFGXgFIKGNJEnAUajcrL3CGT5QdW'
app.config['RECAPTCHA_OPTIONS']= {'theme':'black'}
# ===========DB STUFF========================================================= #
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///arcadia_db.db'
db=SQLAlchemy(app)

class User(db.Model):
	"""
	Represents a users of the app
	"""
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), nullable=False, index=True, unique=True)
	password = db.Column(db.String(50),nullable=False)
	first_name = db.Column(db.String(50), nullable=False)
	last_name = db.Column(db.String(50),nullable=False)
	email = db.Column(db.String(128),nullable=False,unique=True)
	def __repr__(self):
		return "User {}".format(self.username)

# ======== Routing =========================================================== #
# -------- Login ------------------------------------------------------------- #
@app.route('/', methods=['GET', 'POST'])
def login():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            print (request.form)
            username = request.form['username'].lower()
            password = request.form['password']
            if form.validate():
                if validate_password(username, password):
                    session['logged_in'] = True
                    session['username'] = username
                    return json.dumps({'status': 'Login successful'})
                return json.dumps({'status': 'Invalid user/pass'})
            return json.dumps({'status': 'Both fields required'})
        return render_template('login.html', form=form)
    user = helpers.get_user()
    return render_template('home.html', user=user)

@app.route('/add_training_data', methods=['GET', 'POST'])
def get_experiments():
	if not session.get('logged_in'):
		form = forms.LoginForm(request.form)
		if request.method == 'POST':
			print (request.form)
			username = request.form['username'].lower()
			password = request.form['password']
			if form.validate():
				if validate_password(username, password):
					session['logged_in'] = True
					session['username'] = username
					return json.dumps({'status': 'Login successful'})
				return json.dumps({'status': 'Invalid user/pass'})
			return json.dumps({'status': 'Both fields required'})
		return render_template('login.html', form=form)
	user = helpers.get_user()
	response = requests.get("http://localhost:5001/experiments/{}".format(session['username']))
	todos = json.loads(response.text)
	experiments = (todos['experiments'])
	return render_template('add_training_data.html', user=user, experiments=experiments)


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

@app.route("/forgotpassword")
def forgotpassword():
    return "FORGOT PASSWORD PAGE UNDER CONSTRUCTION"

# # -------- Signup ---------------------------------------------------------- #
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if not session.get('logged_in'):
        form = forms.LoginForm(request.form)
        if request.method == 'POST':
            username = request.form['username'].lower()
            #password = helpers.hash_password(request.form['password'])
            password = request.form['password']
            email = request.form['email'].lower()
            if form.validate():
                if user_check(username):
                    if email_check(email):
                        add_user(username, password, email)
                        session['logged_in'] = True
                        session['username'] = username
                        return json.dumps({'status': 'Signup successful'})
                    return json.dumps({'status': 'Email already used'})
                return json.dumps({'status': 'Username taken'})
            return json.dumps({'status': 'Invalid Entry'})
        return render_template('login.html', form=form)
    return redirect(url_for('login'))


# # -------- Settings ---------------------------------------------------------- #
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if session.get('logged_in'):
        if request.method == 'POST':
            password = request.form['password']
            if password != "":
                #password = helpers.hash_password(password)
                password = password
            update_password(get_user().username, password)
            return json.dumps({'status': 'Saved'})
        user = get_user()
        print (user)
        return render_template('settings.html', user=user)
    return redirect(url_for('login'))


# # ======== Main ============================================================== #
if __name__ == "__main__":
    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
