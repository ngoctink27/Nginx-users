from flask import Flask, Response, render_template
from flask import redirect, url_for, request
from flask import jsonify, make_response
from flask import Blueprint

from flask_jwt_extended import create_access_token, jwt_required

from database.models import User
import datetime

theme = Blueprint("theme", __name__)


@theme.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@theme.route("/auth/signup", methods=["GET", "POST"])
def Signup():
    username = request.values.get("username")
    email = request.values.get("email")
    try:
        psw = request.values.get("psw")
        psw_repeat = request.values.get("psw-repeat")
        if psw == psw_repeat and psw:
            password = psw
            user = User(username=username, email=email, password=password)
            user.hash_password()
            user.save()
            return redirect(url_for("Signin"))

        return render_template("signup.html", title="Sign up")

    except:
        return render_template("signup.html", title="Sign up")


@theme.route("/auth/signin", methods=["GET", "POST"])
def Signin():
    token = request.cookies.get("token")
    if token:
        email = request.cookies.get("email")
        return redirect(url_for("theme.success", email=email))

    email = request.values.get("email")
    password = request.values.get("psw")
    if email:
        try:
            user = User.objects.get(email=email)
            authorized = user.check_password(password)
            if not authorized:
                return render_template(
                    "signin.html",
                    title="Sign in",
                    error="Email or password invalid!",
                )
            else:
                expires = datetime.timedelta(days=7)
                access_token = create_access_token(
                    identity=str(user.id), expires_delta=expires
                )
                username = user.username
                user_ip = request.remote_addr
                resp = make_response(
                    render_template(
                        "success.html", username=username, user_ip=user_ip
                    )
                )
                """
                Save to cookie
                """
                resp.set_cookie("token", access_token)
                resp.set_cookie("email", email)
                return resp

        except:
            return render_template(
                "signin.html",
                title="Sign in",
                error="Email or password invalid!",
            )
    return render_template("signin.html", title="Sign in", error="")


@theme.route("/auth/signout", methods=["GET"])
def Signout():
    resp = make_response(
        render_template("signin.html", title="Sign in", error="")
    )
    resp.delete_cookie("token")
    resp.delete_cookie("email")
    return resp


@theme.route("/success", methods=["GET"])
def success():
    email = request.args["email"]
    user = User.objects.get(email=email)
    username = user.username
    user_ip = request.remote_addr

    return render_template("success.html", username=username, user_ip=user_ip)
