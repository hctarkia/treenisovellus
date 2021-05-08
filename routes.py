from app import app
from db import db
from flask import render_template, request, redirect, session
import users, workouts, comments

@app.route("/")
def index():
    results = workouts.get_list()
    return render_template("index.html", results=results)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username,password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3:
            return render_template("error.html", message="Liian lyhyt käyttäjänimi. Sallittu pituus 3-20 merkkiä.")
        elif len(username) > 20:
            return render_template("error.html", message="Liian pitkä käyttäjänimi. Sallittu pituus 3-20 merkkiä.")
        password = request.form["password"]
        if len(password) < 8:
            return render_template("error.html", message="Liian lyhyt salasana. Sallittu pituus 8-20 merkkiä.")
        elif len(password) > 20:
            return render_template("error.html", message="Liian pitkä salasana. Sallittu pituus 8-20 merkkiä.")
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/result")
def result():
    query = request.args["query"]
    if len(query) == 0:
        return render_template("error.html", message="Lisää hakusana")
    elif len(query) > 100:
        return render_template("error.html", message="Liian pitkä hakusana")
    results = workouts.search(query)
    return render_template("result.html", results=results)

@app.route("/add", methods=["POST"])
def add():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", message="Yritit jotain kiellettyä")
    workout = request.form["workout"]
    duration = request.form["duration"]
    description = request.form["description"]
    if len(workout) > 100:
        return render_template("error.html", message="Liian pitkä harjoituksen nimi")
    elif len(workout) == 0:
        return render_template("error.html", message="Lisää harjoituksen nimi")
    if len(description) > 5000:
        return render_template("error.html", message="Liian pitkä kuvaus")
    if int(duration) < 1:
        return render_template("error.html", message="Lisää treenin kesto")
    if workouts.add(workout, duration, description):
        return redirect("/")
    else:
        return render_template("error.html", message="Lisäys ei onnistunut")

@app.route("/profile")
def profile():
    results = workouts.profile()
    return render_template("profile.html", results=results)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/comments")
def show():
    workout_id = request.form["workout_id"]
    workout = workouts.get_workout(workout_id)
    results = comments.get_comments(workout_id)
    return render_template("comment.html", workout=workout, results=results)

@app.route("/add_comment", methods=["POST"])
def comment():
    if session["csrf_token"] != request.form["csrf_token"]:
        return render_template("error.html", message="Yritit jotain kiellettyä")
    workout_id = request.form["workout_id"]
    comment = request.form["comment"]
    if comments.add(workout_id, comment):
        return redirect("/comment")
    else:
        return render_template("error.html", message="Lähetys ei onnistunut")

@app.route("/delete", methods=["POST"])
def delete():
    workout_id = request.form["workout_id"]
    workouts.delete(workout_id)
    return redirect("/")