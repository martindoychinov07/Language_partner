from flask import Flask, render_template, url_for, redirect, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import hashlib
from email_verification import *


app = Flask(__name__)
app.secret_key = "Python"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days = 5)

db = SQLAlchemy(app)


class users(db.Model):
	_id = db.Column("id", db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(100))
	language = db.Column(db.String(100))
	password = db.Column(db.String(100))
	status = db.Column(db.Integer)

	def __init__(self, name, email, language, password, status):
		self.name = name
		self.email = email
		self.language = language
		self.password = password
		self.status = status


@app.route("/")
def home():
	return render_template("home.html")


@app.route("/signup", methods = ["POST", "GET"])
def signup():
	if request.method == "POST":
		session.permanent = True
		user = request.form["user"]
		language = request.form["language"]
		email = request.form["email"]
		password = request.form["password"]
		session["user"] = user
		session["email"] = email
		session["password"] = password
		
		salt = "6hgzas"
		hashed = hashlib.md5((password + salt).encode()).hexdigest()
		found_user = users.query.filter_by(name = user).first()
	    
		if found_user:
			flash("There is already a user with that name! Please choose another!")
		else:
			flash("Verification email was sent!")
			send_email(email)
			usr = users(user, email, language, hashed, 0)
			db.session.add(usr)
			db.session.commit()
			return redirect("verify")
	return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
	if request.method == "POST":
		user = request.form["user"]
		email = request.form["email"]
		password = request.form["password"]
		found_user = users.query.filter_by(name = user).first()
		
		if type(found_user) != None:
			if "user" in session and found_user.status == 1:
				flash("Already logged in!")
			elif "user" in session and found_user.status == 0:
				flash("Account not verified!")
			else:
				session["user"] = user
				session["email"] = email
				session["password"] = password
				salt = "6hgzas"

				hashed = hashlib.md5((password + salt).encode()).hexdigest()

				if found_user:
					if found_user.password == hashed and found_user.email == email and found_user.status == 1:
						flash("Successfully logged in!")
					elif found_user.password != hashed:
						flash("Incorrect password!")
					elif found_user.email != email:
						flash("Incorrect email!")
					elif found_user.status == 0:
						flash("Account not verified!")
				else:
					flash("No such user found! Please sign up first!")
					return render_template("signup.html")
		else:
			flash("No such user found!")
	return render_template("login.html")


@app.route("/logout")
def logout():
	if "user" in session:
		user = session["user"]
		flash(f"You have been logged out, {user}!")
	session.pop("user", None)
	session.pop("email", None)
	session.pop("language", None)
	session.pop("password", None)
	return redirect(url_for("login"))


@app.route("/verify", methods=["POST", "GET"])
def verification():
	if request.method == "POST":
		found_user = users.query.filter_by(name = session["user"]).first()
		num = session["code"]
		ver = request.form["ver"]
		if str(ver) == str(num):
			found_user.status = 1
			db.session.add(found_user)
			db.session.commit()
			flash("Successfully logged in!")
			return render_template("search.html")
		elif ver != num or ver == "":
			flash("Verification code is incorrect! Please try again!")
	return render_template("verification.html")  


@app.route("/view")
def view():
	return render_template("view.html", values = users.query.all())


@app.route("/search", methods=["POST", "GET"])
def search():
	if "user" in session:
		if request.method == "POST":
			searched_language = request.form["s_language"]
			found_language = users.query.filter_by(language = searched_language).first()
			flashed = 0
			if found_language == None:
				flash("There are no users who may know this language!")
				return render_template("search.html")
			
			while found_language != None:
				found_language = users.query.filter_by(language = searched_language).first()
				if found_language:
					if flashed == 0:
						flash("People who may know the language:")
						flashed = 1
					checked = 1
					found_language.language = checked
					flash(found_language.name)
	else:
		flash("You are not logged in!")
		return redirect(url_for("login"))

	return render_template("search.html")


@app.route('/invitation')
def invitation():
	pass


@app.route('/delete')
def delete():
	pass


if __name__ == "__main__":
	db.create_all()
	app.run(debug = True)