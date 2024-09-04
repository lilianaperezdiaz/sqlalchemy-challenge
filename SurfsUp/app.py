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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
measurement = base.classes.measurement
Stations = base.classes.station


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
        f"/api/v1.0/start <br />"
        f"/api/v1.0/start/end <br />"
    )
@app.route("/api/v1.0/precipitation")
def percipitation():
    #Query percipitation data for last 12 months
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year)
    session.close()

    #Create dictionary of percipitation analysis using date as the key and prcp as the value 
    percip_yr = []
    for date, prcp in results:
        prcp_data ={}
        prcp_data["Date"] = date
        prcp_data["Percipitation"] = prcp
        percip_yr.append(prcp_data)
    return jsonify(percip_yr)

@app.route("/api/v1.0/stations")
def Stations():
    #Query stations data 
    station_data = session.query(measurement.station).group_by(measurement.station).all()
    session.close()
    all_stations = []
    for station in station_data:
        station_dict = {}
        station_dict["Station"] = station
        all_stations.append(station_dict)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Query dates and temps of most active station from the previous year
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    max_station = session.query(measurement.date , measurement.tobs).filter(measurement.station == 'USC00519281', measurement.date >= one_year )
    session.close()

    station_data = []
    for date, tobs in max_station:
        temp_data = {}
        temp_data["Date"] = date
        temp_data["Temperature"] = tobs
        station_data.append(temp_data)
    return jsonify(station_data)

@app.route("/api/v1.0/start")
#For a specified start, calculate TMIN, TAVG, and TMAX 
# for all the dates greater than or equal to the start date.
def start():
    start_yr = dt.date(2017,8,23)
    start_info = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date == start_yr)
    session.close()
    start_data = []
    for min, max, avg in start_info:
        str = {}
        str["Min"] = min
        str["Max"] = max
        str["Average"] = avg
        start_data.append(str)
    return jsonify(start_data)

@app.route("/api/v1.0/start/end")
def start_end():
    end_yr = dt.date(2016,8,23)
    end_info = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date == end_yr)
    session.close()
    end_data = []
    for min, max, avg in end_info:
        en = {}
        en["Min"] = min
        en["Max"] = max
        en["Average"] = avg
        end_data.append(en)
    return jsonify(end_data)

if __name__ == '__main__':
    app.run(debug=True)

