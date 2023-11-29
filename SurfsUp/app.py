# Import the dependencies.
import flask
from flask import Flask
from flask import jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func

import datetime as dt
from dateutil.relativedelta import relativedelta

#################################################
# Globals Setup
#################################################
date_format = '%Y-%m-%d'

#################################################
# Helper Methods
#################################################

def get_year_old_date():
    recent_date = session.query(func.max(measurement.date)).all()[0][0]
    return (dt.datetime.strptime(recent_date, date_format) - relativedelta(years=1)).strftime(date_format)

def get_temp_stats(start, end=None):
    query = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.date >= start)
    if end != None:
        query = query.filter(measurement.date <= end)
    result = query.all()[0]
    return result[0], result[1], result[2]

def get_most_active_station():
    return (session.query(measurement.station, func.count(measurement.station))
                    .group_by(measurement.station)
                    .order_by(func.count(measurement.station).desc())
                    .all()[0][0])
                    
def validate_date(date):
    try:
        return dt.datetime.strptime(date, date_format).date()
    except ValueError:
        raise ValueError('{} is not a valid date in the format YYYY-MM-DD'.format(date))

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# # reflect the tables
base = automap_base()
base.prepare(autoload_with=engine)

# # Save references to each table
measurement = base.classes.measurement
station = base.classes.station

# # Create our session (link) from Python to the DB
# # Create a scoped session to autoclean up connections
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

#################################################
# Flask Setup
#################################################

app = Flask(__name__, static_folder=None)

# # Shut down database connections when finished
@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

#################################################
# Flask Routes
#################################################
@app.route("/")
def site_map():
    routes = []

    for rule in app.url_map.iter_rules():
        routes.append('%s' % rule)
    return jsonify(routes)

# Should dates that only have None be removed from response? None means no data, as 0.0 is present in data
@app.route("/api/v1.0/precipitation")
def precipitation():
    year_ago = get_year_old_date()
    precipitation = session.query(measurement.date, measurement.prcp).filter(measurement.date >= year_ago).all()
    cumulative_precipitation= dict()
    for pairs in precipitation:
        date = pairs[0]
        prcp = pairs[1]
        if date in cumulative_precipitation and cumulative_precipitation[date] != None: 
            if prcp != None:
                cumulative_precipitation[date] += prcp
        else: 
            cumulative_precipitation[date]= prcp
    return {"precipitation" : cumulative_precipitation}

# Returning Station IDs
@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()
    response = [station_tuple[0] for station_tuple in stations]
    return jsonify(response)
    
# Returning Most Active Station tobs   
@app.route("/api/v1.0/tobs")
def tobs():
    year_ago = get_year_old_date()
    most_active = get_most_active_station()
    most_active_tobs = session.query(measurement.date, measurement.tobs).filter(measurement.station == most_active).filter(measurement.date >= year_ago).all()
    return {most_active: {"tobs": { pair[0] : pair[1] for pair in most_active_tobs}}}

@app.route("/api/v1.0/<start>")
def temp_start(start):
    try: 
        validate_date(start)
    except ValueError as ex:
        return jsonify({"Error": str(ex)}), 400
    temps_min, temps_max, temps_avg =  get_temp_stats(start)
    return {"Temps Min": temps_min,
            "Temps Max": temps_max,
            "Temps Avg": temps_avg
            }

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    try: 
        if validate_date(end) < validate_date(start):
            return jsonify({"Error": "End date is before start date"}), 400
    except ValueError as ex:
        return jsonify({"Error": str(ex)}), 400
    temps_min, temps_max, temps_avg =  get_temp_stats(start, end)
    return {"Temps Min": temps_min,
            "Temps Max": temps_max,
            "Temps Avg": temps_avg
            }