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


# @app.route("/measles_rate")
# def measles_rate_data():

#     # Query for the top 10 emoji data
#     results = db.session.query(Vaccination.country, Vaccination.measles_rate).\
#         order_by(Vaccination.country.desc()).\
#         limit(100).all()

#     # Create lists from the query results
#     country = [result[0] for result in results]
#     measles_rate = [int(result[1]) for result in results]

#     # Generate the plot trace
#     trace = {
#         "x": country,
#         "y": measles_rate,
#         "mode": "line+markers"
#         "type": "scatter" # make scatter
#     }
#     return jsonify(trace)

# @app.route("/measles_cases")
# def measles_cases_data():

#     # Query for the top 10 emoji data
#     results = db.session.query(Vaccination.country, Vaccination.measles_cases).\
#         order_by(Vaccination.country.desc()).\
#         limit(100).all()

#     # Create lists from the query results
#     country = [result[0] for result in results]
#     measles_cases = [int(result[1]) for result in results]

#     # Generate the plot trace
#     trace = {
#         "x": country,
#         "y": measles_cases,
#         "mode": "line+markers"
#         "type": "scatter" # make scatter
#     }
#     return jsonify(trace)
 
#     # fig = go.Figure(data=go.Scatter(x=data['Country'],
#     #                                 y=data['Measle Rate'],
#     #                                 mode='markers',
#     #                                 marker_color=data['Measle Rate'],
#     #                                 text=data['Country'])) # hover text goes here

#     # fig.update_layout(title='Measle Vaccination Rate around the World')
#     # fig.show()



# @app.route("/polio_rate")
# def polio_rate_data():

#     # Query for the top 10 emoji data
#     results = db.session.query(Vaccination.country, Vaccination.polio_rate).\
#         order_by(Vaccination.country.desc()).\
#         limit(100).all()

#     # Create lists from the query results
#     country = [result[0] for result in results]
#     polio_rate = [int(result[1]) for result in results]

#     # Generate the plot trace
#     trace = {
#         "x": country,
#         "y": polio_rate,
#         "mode": "line+markers"
#         "type": "scatter" # make scatter
#     }
#     return jsonify(trace)

# @app.route("/polio_cases")
# def polio_cases_data():

#     # Query for the top 10 emoji data
#     results = db.session.query(Vaccination.country, Vaccination.polio_cases).\
#         order_by(Vaccination.country.desc()).\
#         limit(100).all()

#     # Create lists from the query results
#     country = [result[0] for result in results]
#     polio_cases = [int(result[1]) for result in results]

#     # Generate the plot trace
#     trace = {
#         "x": country,
#         "y": polio_cases,
#         "mode": "line+markers"
#         "type": "scatter" # make scatter
#     }
#     return jsonify(trace)


@app.route("/measles_cases")
def measle_cases_data():
    """Return country name and measle rate for that country"""

    # Query data
    results = (db.session.query(Vaccination.Year, Vaccination.Total_Polio_Cases, Vaccination.Country)
        .filter(Vaccination.Country == 'China').order_by(Vaccination.Year.desc())
        .all())
    df = pd.DataFrame(results, columns=['Year', 'Total Polio Cases', 'Country'])

    
    # Format the data for Plotly
    plot_trace = {
        "x": df["Year"].values.tolist(),
        "y": df["Total Polio Cases"].values.tolist(),
        "mode": "line + markers",
        "type": "scatter"
    }
    return jsonify(plot_trace)


if __name__ == '__main__':
    app.run(debug=True)
