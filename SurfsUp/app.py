# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement
stations = base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes"""
    return(
        f"Available Routes: <br />"
        f"/api/v1.0/precipitation <br />"
        f"/api/v1.0/stations <br />"
        f"/api/v1.0/tobs <br />"
        f"/api/v1.0/<start> <br />"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def percipitation():
    #Query percipitation data for last 12 months
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= one_year).all()
    session.close()

    #Create dictionary of percipitation analysis using date as the key and prcp as the value 
    percip_yr = []
    for date, prcp in results:
        prcp_data ={}
        prcp_data["Date"] = date
        prcp_data["Percipitation"] = prcp
        percip_yr.append(prcp_data)
    return jsonify(percip_yr)

if __name__ == '__main__':
    app.run(debug=True)

