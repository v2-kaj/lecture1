import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgres+psycopg2://dba:kajani1993@localhost/lecture2")
db = scoped_session(sessionmaker(bind=engine))
engine.connect()

@app.route("/")
def index():
    flights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flightid = int(request.form.get("fid"))
    except ValueError:
        return render_template("error.html", message="Invalid Flight Number.")
    if db.execute("SELECT * FROM flights WHERE id =:id", {"id": flightid}).rowcount==0:
        return render_template("error.html", message="No such flight with that ID.")
    db.execute("INSERT INTO passengers (name, flightid ) VALUES (:name, :flightid)",
            {"name" : name, "flightid":flightid})
    db.commit()
    return render_template("success.html")
@app.route("/flights")
def flights():
    allflights = db.execute("SELECT * FROM flights").fetchall()
    return render_template("flights.html", flights=allflights)

@app.route("/flights/<int:flightid>")
def flight(flightid):
    flight = db.execute("SELECT * FROM flights WHERE id = :id", {"id": flightid}).fetchone()
    if flight is None:
        return render_template("error.html", message="No such flight.")
    passengers = db.execute("SELECT name FROM passengers WHERE flightid =:id", {"id": flightid}).fetchall()
    return render_template("flight.html", flight=flight, passengers=passengers)
