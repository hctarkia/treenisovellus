from app import app
from flask import render_template, request, redirect
import users

@app.route("/")
def index():
    return render_template("index.html")

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

@app.route("/new", methods=["POST"])
def new():
    return render_template("new.html")

@app.route("/result")
def result():
    query = request.args["query"]
    sql = "SELECT date, workout, duration, description FROM workouts WHERE workout LIKE :query"
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    workouts = result.fetchall()
    return render_template("result.html",workouts=workouts)

@app.route("/add", methods=["POST"])
def add():

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/search")
def search():
    return render_template("search.html")