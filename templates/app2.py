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


@app.route("/")
def home():
    """Render Home Page."""
    return render_template("Charts.html")


@app.route("/usa")
def usa_data():
    """Return country name and measle rate for that country"""

    # Query data
    results = (db.session.query(Vaccination.Year, Vaccination.Total_Measle_Cases, Vaccination.Country)
        .filter(Vaccination.Country == 'USA').order_by(Vaccination.Year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Total Measle Cases', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Total Measle Cases"].values.tolist(),
        "mode": "line + markers",
        "type": "scatter"
    }
    return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)
