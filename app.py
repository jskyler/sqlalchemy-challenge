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
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"TOBs: /api/v1.0/tobs<br/>"
        f"Start Date: /api/v1.0/&#60;yyyy-mm-dd&#62;<br/>"
        f"Start/End Date: /api/v1.0/&#60;yyyy-mm-dd&#62;/&#60;yyyy-mm-dd&#62;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query all precipitation
    prcp_results = session.query(Measurement.date,Measurement.prcp).all()
        
    all_prcp = []
    for date, prcp in prcp_results:
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

    # Find last date and one year back
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_date = dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()
    
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > one_year_date).filter(Measurement.station==most_active_station[0]).all()
    
    return jsonify(tobs_results)


@app.route('/api/v1.0/<start>')
def start_date(start):
    
    start_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    all_tobs = []
    for min, max, avg in start_results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Max"] = max
        tobs_dict["Average"] = avg
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)


@app.route('/api/v1.0/<start>/<end>')
def start_end_date(start,end):
    
    start_end_results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    all_tobs = []
    for min, max, avg in start_end_results:
        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Max"] = max
        tobs_dict["Average"] = avg
        all_tobs.append(tobs_dict)
        
    return jsonify(all_tobs)
    

if __name__ == '__main__':
    app.run(debug=True)