#FLASK
from flask import Flask, jsonify, render_template, request
app = Flask(__name__)
import os,optparse
import yaml

info = {}

# developer = os.getenv("DEVELOPER", "Me")
developer=os.getenv("DEVELOPER")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/details")
def details():
    return render_template("details.html")

@app.route("/movies")
def movies():
    return render_template("movies.html")

if __name__ == "__main__":
    debug=False
    app.run(host="0.0.0.0",debug=debug)