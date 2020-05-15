from flask import Flask, render_template, request
from models import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "postgres+psycopg2://admin:kajani1993@localhost/lecture5"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db.init_app(app)

@app.route("/")
def index():
    flights = Flight.query.order_by(Flight.origin).all()
    return render_template("index.html", flights=flights)

@app.route("/book", methods=["POST"])
def book():
    name = request.form.get("name")
    try:
        flightid = int(request.form.get("fid"))
    except ValueError:
        return render_template("error.html", message="Invalid Flight Number.")

    flight = Flight.query.get(flightid)
    if flight is None:
        return render_template("error.html", message="Invalid ID.")

    flight.add_passenger(name)
    return render_template("success.html")
@app.route("/flights")
def flights():
    allflights = Flight.query.order_by(Flight.origin).all()
    return render_template("flights.html", flights=allflights)

@app.route("/flights/<int:flightid>")
def flight(flightid):
    flight = Flight.query.get(flightid)
    if flight is None:
        return render_template("error.html", message="No such flight.")
    passengers = flight.passengers
    return render_template("flight.html", flight=flight, passengers=passengers)
