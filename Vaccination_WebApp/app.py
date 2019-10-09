import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify)

from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import create_engine # refer to hw 10

app = Flask(__name__)

# The database URI
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:Yahoo!098@localhost/project_2" #postgresaql?

db = SQLAlchemy(app)

#engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

# Create our database model
class Vaccination(db.Model):
    __tablename__ = 'vaccination' #postgres table name

    #change names to match columns on postgres
    id = db.Column(db.Integer, primary_key=True)
    Measle_Vaccinated_Rate = db.Column(db.Integer)
    Polio_Vaccination_Rate = db.Column(db.Integer)
    Total_Measle_Cases = db.Column(db.Integer)
    Total_Polio_Cases = db.Column(db.Integer)
    Country = db.Column(db.String)
    Year = db.Column(db.Integer)

#not neccessary unless printing to console
    def __repr__(self):
        return '<Vaccination %r>' % (self.country)


# Create database tables
# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     # db.drop_all()
#     db.create_all()


@app.route("/")
def home():
    """Render Home Page."""
    return render_template("index.html") # Heather to do html/css

# List of countries 
countries_list = db.session.query(Vaccination.Country).distinct() #display unique country names

# Measle Vaccination Rate function

def measles_vaccination(Country):
    """Return country name and measle rate for that country"""

    # Query data
    results = (db.session.query(Vaccination.Year, Vaccination.Measle_Vaccinated_Rate, Vaccination.Country)
        .filter(Vaccination.Country == Country).order_by(Vaccination.Year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Measles Vaccinated Rate', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Measles Vaccinated Rate"].values.tolist(),
        "mode": "line + markers",
        "type": "scatter"
    }
    return plot_trace

# Measle Rate function

def measles_cases(Country):
    """Return country name and measle rate for that country"""

    # Query data
    results = (db.session.query(Vaccination.Year, Vaccination.Total_Measle_Cases, Vaccination.Country)
        .filter(Vaccination.Country == Country).order_by(Vaccination.Year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Number of Measle Cases', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Number of Measle Cases"].values.tolist(),
        "mode": "line + markers",
        "type": "scatter"
    }
    return plot_trace

# Polio Vaccination Rate function

def polio_vaccination(Country):
    """Return country name and measle rate for that country"""

    # Query data
    results = (db.session.query(Vaccination.Year, Vaccination.Polio_Vaccination_Rate, Vaccination.Country)
        .filter(Vaccination.Country == Country).order_by(Vaccination.Year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Polio Vaccinated Rate', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Polio Vaccinated Rate"].values.tolist(),
        "mode": "line + markers",
        "type": "scatter"
    }
    return plot_trace

# Polio Rate function

def polio_cases(Country):
    """Return country name and measle rate for that country"""

    # Query data
    results = (db.session.query(Vaccination.Year, Vaccination.Total_Polio_Cases, Vaccination.Country)
        .filter(Vaccination.Country == Country).order_by(Vaccination.Year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Number of Polio Cases', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Number of Polio Cases"].values.tolist(),
        "mode": "line + markers",
        "type": "scatter"
    }
    return plot_trace

@app.route("/get_plots/<Country>")
def function(Country):
    # dicts
    {
    measles_rate_graph : measles_vaccination,
    measles_cases_graph : measles_cases,
    polio_rate_graph : polio_vaccination,
    polio_cases_graph : polio_cases
    }
    return jsonify ({'trace_1': measles_rate_graph, 'trace_2': measles_cases_graph, 'trace_3': polio_rate_graph, 'trace_4': polio_cases_graph})
    # return jsonify ("Test")

if __name__ == '__main__':
    app.run(debug=True)
