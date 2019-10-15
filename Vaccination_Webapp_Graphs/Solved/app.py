import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect



from flask import (
    Flask,
    render_template,
    jsonify)

app = Flask(__name__)



#################################################
# Database Setup
#################################################
# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:Yahoo!098@localhost/project_2" #three slahes?
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


inspector =inspect(engine)
print(inspector.get_table_names())


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measle_Vaccination = Base.classes.measles_vaccination
# Measle_Cases = Base.classes.measle_cases
# Polio_Rate = Base.classes.polio_rate
# Polio_Cases = Base.classes.polio_cases
#Vaccination = Base.classes.vaccination

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
def home():
    """Render Home Page."""
    return render_template("index.html") # Heather to do html/css


@app.route("/measles_vaccination")
def measle_vaccination_data():
    """Return country name and measle rate for that country"""

    # Query data
    results = (session.query(Measle_Vaccination.year, Measle_Vaccination.measle_vaccinated_rate, Measle_Vaccination.country)
        .filter(Measle_Vaccination.country == 'USA').order_by(Measle_Vaccination.year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Measles Vaccinated Rate', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Measles Vaccinated Rate"].values.tolist(),
         "mode": "line+markers",
        "type": "scatter"
    }
    return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)

