from app import app
from db import db
from flask import render_template, request, redirect
import users, workouts

@app.route("/")
def index():
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description FROM users u, workouts w WHERE u.id=w.user_id ORDER BY w.id DESC"
    result = db.session.execute(sql)
    results = result.fetchall()
    return render_template("index.html",results=results)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username,password):
            return redirect("/")
        else:
            return render_template("error.html",message="Rekisteröinti ei onnistunut")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description FROM users u, workouts w WHERE u.id=w.user_id AND workout LIKE :query ORDER BY w.id DESC"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    results = result.fetchall()
    return render_template("result.html",results=results)

@app.route("/add", methods=["POST"])
def add():
    workout = request.form["workout"]
    duration = request.form["duration"]
    description = request.form["description"]
    if len(workout) > 100:
        return render_template("error.html",message="Liian pitkä harjoituksen nimi")
    elif len(workout) == 0:
        return render_template("error.html",message="Lisää treenin nimi")
    if len(description) > 5000:
        return render_template("error.html",message="Liian pitkä kuvaus")
    if duration < 1:
        return render_template("error.html",message="Lisää treenin kesto")
    if workouts.add(workout, duration, description):
        return redirect("/")
    else:
        return render_template("error.html",message="Lisäys ei onnistunut")

@app.route("/profile")
def profile():
    user = users.user_id()
    sql = "SELECT u.username, w.date, w.workout, w.duration, w.description FROM users u, workouts w WHERE u.id=w.user_id AND u.id='"+user+"' ORDER BY w.id DESC"
    result = db.session.execute(sql)
    results = result.fetchall()
    return render_template("profile.html",results=results)

@app.route("/search")
def search():
    return render_template("search.html")