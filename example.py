from flask import Flask, render_template, url_for, redirect, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import hashlib
from email_verification import *
from notification import *


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
	invitations = db.Column(db.String(1000))
	friends = db.Column(db.String(1000))

	def __init__(self, name, email, language, password, status, invitations, friends):
		self.name = name
		self.email = email
		self.language = language
		self.password = password
		self.status = status
		self.invitations = invitations
		self.friends = friends


@app.route("/signup", methods = ["POST"])
def signup():
	if request.method == "POST":
		user_data = request.json
		session.permanent = True
		user = user_data["name"]
		email = user_data["email"]
		password = user_data["password"]
		language = user_data["language"]
		session["user"] = user
		session["email"] = email
		session["password"] = password
		
		salt = "6hgzas"
		hashed = hashlib.md5((password + salt).encode()).hexdigest()
		found_user = users.query.filter_by(name = user).first()
	    
		if found_user:
			return (jsonify(type = "error", message = "user.exists"))
		else:
			send_email(email)
			usr = users(user, email, language, hashed, 1, "", "")
			db.session.add(usr)
			db.session.commit()
			
	return jsonify(name = user, language = language, email = email, password = password) 


@app.route("/login", methods=["POST"])
def login():
	if request.method == "POST":
		user_data = request.json
		user = user_data["name"]
		email = user_data["email"]
		password = user_data["password"]
		found_user = users.query.filter_by(name = user).first()
		
		if type(found_user) != None:
			if "user" in session and found_user.status == 1:
				return jsonify(type = "warning", message = "user.already.logged.in")
			elif "user" in session and found_user.status == 0:
				return jsonify(type = "error", message = "account.not.verified")
			else:
				salt = "6hgzas"

				hashed = hashlib.md5((password + salt).encode()).hexdigest()

				if found_user:
					if found_user.password == hashed and found_user.email == email and found_user.status == 1:
						session["user"] = user
						session["email"] = email
						session["password"] = password
						return jsonify(type = "warning", message = "successfully.logged.in")
					elif found_user.password != hashed:
						return jsonify(type = "error", message = "incorrect.password")
					elif found_user.email != email:
						return jsonify(type = "error", message = "incorrect.email")
					elif found_user.status == 0:
						return jsonify(type = "error", message = "account.not.verified")
				else:
					return jsonify(type = "error", message = "user.not.found")
		else:
			return jsonify(type = "error", message = "no.such.user")
	
	return jsonify(type = "warning", message = "logged.in")


@app.route("/logout", methods=["POST", "GET"])
def logout():
	if "user" in session:
		session.pop("user", None)
		session.pop("email", None)
		session.pop("language", None)
		session.pop("password", None)
		return jsonify(type = "warning", message = "user.logged.out")


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
			return jsonify(type = "warning", message = "logged.in")
		elif ver != num or ver == "":
			return jsonify(type = "error", message = "code.incorrect")


@app.route("/search", methods=["POST"])
def search():
	if "user" in session:
		if request.method == "POST":
			user_data = request.json
			searched_language = user_data["language"]
			found_language = users.query.filter_by(language = searched_language).first()
			if found_language == None:
				return jsonify(type = "error", message = "no.users.with.that.language")
			
			while found_language != None:
				found_language = users.query.filter_by(language = searched_language).first()
				if found_language:
					checked = 1
					found_language.language = checked
					return jsonify(user = found_language.name)
	else:
		return jsonify(type = "error", message = "not.logged.in")
	

@app.route('/profile', methods=["POST"])
def profile():
	if request.method == "POST":
		if "user" in session:
			found_user = users.query.filter_by(name = session["user"]).first()
			return jsonify(name = found_user.name, language = found_user.language, email = found_user.email, invitations = found_user.invitations, friends = found_user.friends)
		else:
			return jsonify(type = "error", message = "not.logged.in")


@app.route('/invite', methods=["POST"])
def invite():
	if request.method == "POST":
		user_data = request.json
		invited = user_data["invited"]
		active_user = session["user"]
		found_user = users.query.filter_by(name = invited).first()
		if found_user != None:
			if active_user not in found_user.invitations and found_user.name != session["user"]:
				found_user.invitations = found_user.invitations + active_user + " " 
				send_notification(found_user.email)
				db.session.add(found_user)
				db.session.commit()
			elif found_user.name == session["user"]:
				return jsonify(type = "error", message = "user.invited.himself")
			elif active_user in found_user.invitations:
				return jsonify(type = "error", message = "invitation.already.sent")
			return jsonify(invited = found_user.name, active = active_user)
		else:
			return jsonify(type = "error", message = "user.not.found")


@app.route("/invitation", methods = ["POST"])
def invitation():
	if request.method == "POST":
		user_data = request.json
		accepted = user_data["accepted"]
		user = session["user"]
		found_user = users.query.filter_by(name = user).first()
		if (accepted + " ") in found_user.invitations and (accepted + " ") not in found_user.friends:
			found_user.friends = found_user.friends + accepted + " "
			temp = found_user.invitations.split()
			temp.remove(accepted)
			for i in temp:
				found_user.invitations = found_user.invitations + i
			if len(str(temp)) == 0 or str(temp) == "[]":
				found_user.invitations = ""
			db.session.add(found_user)
			db.session.commit()
		elif (accepted + " ") in found_user.friends:
			return jsonify(type = "error", message = "invitation.accepted.already")
		else:
			return jsonify(type = "error", message = "no.such.invitation")
		
		if "user" not in session:
			return jsonify(type = "error", message = "not.logged.in")
	
	return jsonify(name = found_user.name, friends = found_user.friends)


@app.route('/delete', methods = ["POST"])
def delete():
	if request.method == "POST":
		user_data = request.json
		answer = user_data["answer"]
		if "user" in session:
			if answer == 1:
				found_user = users.query.filter_by(name = session["user"]).first()
				db.session.delete(found_user)
				db.session.commit()
				session.pop("user", None)
				session.pop("email", None)
				session.pop("language", None)
				session.pop("password", None)
		else:
			return jsonify(type = "error", message = "not.logged.in")

	return jsonify(type = "warning", message = "account.deleted")


if __name__ == "__main__":
	db.create_all()
	app.run(debug = True)