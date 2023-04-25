from flask import Blueprint, request, redirect, url_for
from ..models import User, db
from ..manager.security_manager import bcrypt
from sqlalchemy.exc import IntegrityError
import flask_login

accounts = Blueprint("account", __name__)

@accounts.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
               <form action="login" method="POST">
                <input type="text" name="username" id="username" placeholder="username"/>
                <input type="password" name="password" id="password" placeholder="password"/>
                <input type="submit" name="submit"/>
               </form>
               """

    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    
    if bcrypt.check_password_hash(pw_hash=user.password, password=password):
        flask_login.login_user(user)
        return redirect(url_for("account.protected"))
    return "Bad login"

@accounts.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return """
               <form action="register" method="POST">
                <input type="text" name="username" id="username" placeholder="username"/>
                <input type="password" name="password" id="password" placeholder="password"/>
                <input type="submit" name="submit"/>
               </form>
               """

    username = request.form.get("username")
    password = bcrypt.generate_password_hash(request.form.get("password"))
    user = User(username=username, password=password)
    try:
        db.session.add(user)
        db.session.commit()
        flask_login.login_user(user)
        return redirect(url_for("account.protected"))
    except IntegrityError:
        return "Username is already in use!"

@accounts.route("/protected")
@flask_login.login_required
def protected():
    return f"Logged in as {flask_login.current_user.username}" 

@accounts.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out."