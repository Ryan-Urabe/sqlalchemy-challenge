# Import the dependencies.

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, distinct, desc

from flask import Flask, render_template, jsonify


#################################################
# Database Setup
#################################################


engine = create_engine("sqlite:///Resources/Hawaii.sqlite")

base = automap_base()

base.prepare(engine, reflect=True)

measurement = base.classes.measurement

station = base.classes.station


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")

def home():
    """List all Available api routes."""
    return (
        f"Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    results = session.query(measurement.date, measurement.prcp). order_by(measurement.date).all()
    
    rain_date_list = []
    
    for date, prcp in results:
        dict = {}
        dict[date] = prcp
        rain_date_list.append(dict)
    session.close()
        
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stations = {}

    results = session.query(station.station, station.name).all()
    for i, name in results:
        stations[i] = name

    session.close()

    return jsonify(stations)

@ app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    select = [measurement.date, measurement.tobs]
    results = session.query(*select).filter(func.strftime(measurement.date) >= '2016-08-24').all()
    temps = []
    for date, tobs in results:
        dict = {}
        dict["date"] = date
        dict["temp"] = tobs
        temps.append(dict)
    
    session.close()
    return jsonify(temps)

# can't figure this out

if __name__ == "__main__":
    app.run(debug=True)