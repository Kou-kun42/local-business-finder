from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import PrettyPrinter
import urllib.request
import xml.etree.ElementTree as ET
import requests
import json
import os

# Setup

app = Flask(__name__)

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USERID = os.getenv('USERID')

pp = PrettyPrinter(indent=4)


# Flask routes

@app.route('/')
def home():
    '''Display homepage'''
    return render_template('home.html')


@app.route('/about')
def about():
    '''Display about page'''
    return render_template('about.html')


@app.route('/login')
def login():
    '''Display login page'''
    return render_template('login.html')


@app.route('/signup')
def signup():
    '''Display signup page'''
    return render_template('signup.html')


@app.route('/results')
def results():
    '''Display result page'''
    query = request.args.get("search-query")
    city = request.args.get("city")

    # Looking up City and State using USPS api
    usps_requestXML = f"""
    <?xml version="1.0"?>
    <CityStateLookupRequest USERID={USERID}>
        <ZipCode ID= "0">
            <Zip5>17404</Zip5>
        </ZipCode>
    </CityStateLookupRequest>
    """

    docString = usps_requestXML.replace(' ', '')
    docString = urllib.parse.quote_plus(docString)

    usps_url = """
    http://production.shippingapis.com/ShippingAPITest.dll?API=
    CityStateLookup&XML=""" + docString

    usps_url = usps_url.replace('\n', '').replace(' ', '')

    response = urllib.request.urlopen(usps_url)
    contents = response.read()
    print(contents)

    url = "https://api.foursquare.com/v2/venues/explore"

    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "query": query,
        "near": "Chicago, IL",
        "v": 20210201
    }

    results_json = requests.get(url, params=params).json()
    # pp.pprint(results_json)

    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)
