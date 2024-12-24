from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)   # Create a new instance of the Flask class

stations = pd.read_csv("data/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]

@app.route('/')          # Define the URL route for the root of the site
def home():
    return render_template("home.html", data=stations.to_html()) # Return the rendered template

@app.route("/api/v1/<station>/<date>")          # Define the URL route for the root of the site
def about(station, date):
    filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() / 10
    return {"station": station,
             "date": date, 
             "temperature": temperature}

@app.route("/api/v1/<station>")          # Define the URL route for the root of the site
def all_data(station):
    filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    return {"station": station,
            "data": df.to_dict(orient="records")}


@app.route('/api/v1/yearly/<station>/<year>')
def year_data(station, year):
    filename = "data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    df = df.loc[df["    DATE"].dt.year == int(year)]
    return {"station": station,
            "year": year,
            "data": df.to_dict(orient="records")}

if __name__ == "__main__":
    app.run(debug=True, port=5000)   # Start the Flask server

