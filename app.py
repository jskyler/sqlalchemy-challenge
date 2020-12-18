# Import Dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite",connect_args={'check_same_thread': False}, echo=True)
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create the session
session = Session(engine)

# Flask Setup
app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query all precipitation
    prcp_results = session.query(Measurement.prcp).all()
    
    all_prcp = []
    for (date, prcp) in prcp_results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_prcp.append(prcp_dict)

    
    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():

    # Query all stations
    station_results = session.query(Station.station).all()
    
    all_stations = list(np.ravel(station_results))
    
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    # Query all tobs
    tobs_results = session.query(Measurement.tobs).all()
    
    
@app.route("/api/v1.0/<start>")
def start():

    # Query all tobs
    start_results = session.query(Measurement.tobs).all()
    

if __name__ == '__main__':
    app.run(debug=True)