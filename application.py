import os
import requests
import json
from bs4 import BeautifulSoup

from flask import Flask, session, render_template, request
from flask_session import Session

app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.route("/")
def search():
    return render_template("search.html")


@app.route("/result", methods=["POST"])
def result():
    url = request.form.get("search")

    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    repo = soup.find_all('div', class_='d-inline-block mb-1')

    repo2 = soup.find_all('div', id='readme')
    return render_template('result.html', repo=repo, repo2=repo2)
