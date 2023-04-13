from flask import Flask, request, session, jsonify, make_response
# from flask_cors import CORS
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import hashlib
import datetime
import os
from flask_cors import CORS

# from email_verification import *
# from notification import *

app = Flask(__name__, static_folder='../build', static_url_path='/')
# CORS(app)
app.secret_key = "Python"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=5)
CORS(app)
db = SQLAlchemy(app)
app.app_context().push()


class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    known_language = db.Column(db.String(100))
    wanted_language = db.Column(db.String(100))
    password = db.Column(db.String(100))
    status = db.Column(db.Integer)

    def __init__(self, name, email, known_language, wanted_language, password, status):
        self.name = name
        self.email = email
        self.known_language = known_language
        self.wanted_language = wanted_language
        self.password = password
        self.status = status


class chat(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    message = db.Column(db.String(100))
    date = db.Column(db.String(100))
    status = db.Column(db.Integer)

    def __init__(self, sender, receiver, message, date, status):
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.date = date
        self.status = status


class invitations(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    sender = db.Column(db.String(100))
    receiver = db.Column(db.String(100))
    date = db.Column(db.String(100))
    status = db.Column(db.Integer)

    def __init__(self, sender, receiver, date, status):
        self.sender = sender
        self.receiver = receiver
        self.date = date
        self.status = status


class friends(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    accepted = db.Column(db.String(100))
    sent = db.Column(db.String(100))
    date = db.Column(db.String(100))

    def __init__(self, accepted, sent, date):
        self.accepted = accepted
        self.sent = sent
        self.date = date


# @app.route('/')
# def index():
# 	return app.send_static_file('index.html')


@app.route("/api/signup", methods=["POST"])
def signup():
    if request.method == "POST":
        if "user" in session:
            return jsonify(type="error", message="already.logged.in")
        else:
            user_data = request.json
            session.permanent = True
            user = user_data["name"]
            email = user_data["email"]
            password = user_data["password"]
            known_language = user_data["known_language"]
            wanted_language = user_data["wanted_language"]

            session["user"] = user
            session["email"] = email
            session["password"] = password

            salt = "6hgzas"
            hashed = hashlib.md5((password + salt).encode()).hexdigest()
            found_user = users.query.filter_by(name=user).first()

            if found_user:
                return (jsonify(type="error", message="user.exists"))
            else:
                # send_email(email)
                usr = users(user, email, known_language,
                            wanted_language, hashed, 1)
                db.session.add(usr)
                db.session.commit()
            response = make_response(jsonify(name=user, kn_language=known_language, w_language=wanted_language,
                                     email=email, password=password), 201)
    return response


@app.route("/api/login", methods=["POST"])
def login():
    if request.method == "POST":
        user_data = request.json
        user = user_data["name"]
        email = user_data["email"]
        password = user_data["password"]
        found_user = users.query.filter_by(name=user).first()

        if type(found_user) != None:
            if "user" in session and found_user.status == 1:
                return jsonify(type="warning", message="user.already.logged.in")
            elif "user" in session and found_user.status == 0:
                return jsonify(type="error", message="account.not.verified")
            else:
                salt = "6hgzas"

                hashed = hashlib.md5((password + salt).encode()).hexdigest()

                if found_user:
                    if found_user.password == hashed and found_user.email == email and found_user.status == 1:
                        session["user"] = user
                        session["email"] = email
                        session["password"] = password
                        return jsonify(type="warning", message="successfully.logged.in")
                    elif found_user.password != hashed:
                        return jsonify(type="error", message="incorrect.password")
                    elif found_user.email != email:
                        return jsonify(type="error", message="incorrect.email")
                    elif found_user.status == 0:
                        return jsonify(type="error", message="account.not.verified")
                else:
                    return jsonify(type="error", message="user.not.found")
        else:
            return jsonify(type="error", message="no.such.user")

    return jsonify(type="warning", message="logged.in")


@app.route("/api/logout", methods=["POST", "GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
        session.pop("email", None)
        session.pop("kn_language", None)
        session.pop("w_language", None)
        session.pop("password", None)
        return jsonify(type="warning", message="user.logged.out")


@app.route("/api/verify", methods=["POST", "GET"])
def verification():
    if request.method == "POST":
        found_user = users.query.filter_by(name=session["user"]).first()
        num = session["code"]
        ver = request.form["ver"]
        if str(ver) == str(num):
            found_user.status = 1
            db.session.add(found_user)
            db.session.commit()
            return jsonify(type="warning", message="logged.in")
        elif ver != num or ver == "":
            return jsonify(type="error", message="code.incorrect")


@app.route("/api/search", methods=["POST"])
def search():
    if request.method == "POST":
        data = request.json
        kn_language = data["kn_language"]
        found_users = []
        if "user" in session:
            found_user = users.query.filter_by(
                known_language=kn_language).all()
            for i in range(len(found_user)):
                if found_user[i].name != session["user"]:
                    found_users.append(found_user[i].name)
            return jsonify(found_users)
        else:
            return jsonify(type="error", message="not.logged.in")


def get_friends(user):
    found_friends = []
    found_friend = friends.query.filter_by(accepted=user).all()
    for i in range(len(found_friend)):
        found_friends.append(found_friend[i].sent)
    return found_friends


@app.route('/api/profile', methods=["POST"])
def profile():
    if request.method == "POST":
        if "user" in session:
            found_user = users.query.filter_by(name=session["user"]).first()
            if found_user.status == 1:
                user_data = {
                    "name": found_user.name,
                    "email": found_user.email,
                    "kn_language": found_user.known_language,
                    "w_language": found_user.wanted_language
                }
                friends_list = get_friends(session["user"])
                return jsonify(user_data, friends_list)
            else:
                return jsonify(type="error", message="account.not.verified")
        else:
            return jsonify(type="error", message="not.logged.in")


@app.route('/api/invite', methods=["POST"])
def invite():
    if request.method == "POST":
        found_user = users.query.filter_by(name=session["user"]).first()
        if found_user.status == 1:
            if "user" in session:
                user_data = request.json
                receiver = user_data["receiver"]
                sender = session["user"]
                found_invitation = invitations.query.filter_by(
                    sender=sender).first()
                if found_invitation:
                    return jsonify(type="error", message="invitation.already.sent")
                if receiver == sender:
                    return jsonify(type="error", message="user.cant.invite.himself")
                found_user = users.query.filter_by(name=receiver).first()
                date = datetime.datetime.now()
                if found_user != None:
                    new_invite = invitations(sender, receiver, date, 0)
                    db.session.add(new_invite)
                    db.session.commit()
                    return jsonify(type="warning", message="invitation.sent")
                else:
                    return jsonify(type="error", message="user.not.found")
            else:
                return jsonify(type="error", message="not.logged.in")
        else:
            return jsonify(type="error", message="account.not.verified")


@app.route("/api/invitation", methods=["GET", "POST"])
def invitation():
    if request.method == "GET":
        found_user = users.query.filter_by(name=session["user"]).first()
        if found_user.status == 1:
            if "user" in session:
                user = session["user"]
                user_invitations = []
                found_invitation = invitations.query.filter_by(
                    receiver=user).all()
                for i in range(len(found_invitation)):
                    user_invitations.append(found_invitation[i].sender)
                return jsonify(user_invitations)
            else:
                return jsonify(type="error", message="not.logged.in")
        else:
            return jsonify(type="error", message="account.not.verified")

    if request.method == "POST":
        found_user = users.query.filter_by(name=session["user"]).first()
        if found_user.status == 1:
            if "user" in session:
                info = request.json
                user = session["user"]
                accepted = info["accepted"]
                found_invitation = invitations.query.filter_by(
                    sender=accepted, receiver=user).first()
                date = datetime.datetime.now()
                if found_invitation and found_invitation.status == 0:
                    found_invitation.status = 1
                    new_friend = friends(user, accepted, date)
                    db.session.add(found_invitation)
                    db.session.add(new_friend)
                    db.session.commit()
                    return jsonify(type="warning", message="invitation.accepted")
                elif not found_invitation:
                    return jsonify(type="error", message="no.such.invitation.found")
                else:
                    return jsonify(type="error", message="invitation.already.accepted")
            else:
                return jsonify(type="error", message="not.logged.in")
        else:
            return jsonify(type="error", message="account.not.verified")
    return jsonify(type="error")


@app.route('/api/delete', methods=["POST"])
def delete():
    if request.method == "POST":
        user_data = request.json
        answer = user_data["answer"]
        if "user" in session:
            if answer == 1:
                found_user = users.query.filter_by(
                    name=session["user"]).first()
                db.session.delete(found_user)
                db.session.commit()
                session.pop("user", None)
                session.pop("email", None)
                session.pop("kn_language", None)
                session.pop("kn_language", None)
                session.pop("password", None)
        else:
            return jsonify(type="error", message="not.logged.in")

    return jsonify(type="warning", message="account.deleted")


@app.route("/api/chat", methods = ["GET", "POST"])
def chat_func():
	if request.method == "POST":
		chat_data = request.json
		sender = session["user"]
		receiver = chat_data["receiver"]
		message = chat_data["message"]
		if sender == receiver:
			return jsonify(type = "error", message = "user.cant.text.himself")
		date = datetime.datetime.now()
		msg = chat(sender, receiver, message, date, 0)
		db.session.add(msg)
		db.session.commit()
		return jsonify(type = "warning", message = "message.delivered")
	
	if request.method == "GET":
		wanted_data = request.json
		wanted_receiver = session["user"]
		messages = []

		found_messages = chat.query.filter_by(receiver = wanted_receiver, status = 0).all()

		for i in range(len(found_messages)):
			if found_messages[i]:
				found_messages[i].status = 1
				db.session.add(found_messages[i])
				db.session.commit()
				messages.append({"message": found_messages[i].message, "sender": found_messages[i].sender, "time" : found_messages[i].date})
		if found_messages == []:
			return jsonify(type = "error", message = "no.messages.for.that.user")
		return jsonify(messages)
	return jsonify(type = "error", message = "no.messages.found")


if __name__ == "__main__":
    # db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
