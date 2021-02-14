from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import PrettyPrinter
import requests
import json
import os

# Setup

app = Flask(__name__)

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

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
    zipcode = request.args.get("zipcode")

    # Looking up City and State using Ziptastic api
    zipurl = "http://ZiptasticAPI.com/" + str(zipcode)
    zip_json = requests.get(zipurl).json()
    # Getting city and state from result json
    city = zip_json["city"]
    state = zip_json["state"]
    location = f"{city}, {state}"

    # Foursquare places api url
    url = "https://api.foursquare.com/v2/venues/search"
    photo_url = "https://api.foursquare.com/v2/venues/VENUE_ID/photos"
    # Parameters for the venues api
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "query": query,
        "near": location,
        "v": 20210201,
        "limit": 3
    }
    
    results_json = requests.get(url, params=params).json()
    print('----------------')
    pp.pprint(results_json)
    pp.pprint(results_json['response']['venues'][0]['id'])
    print('---------------')
    venue_id = results_json['response']['venues'][0]['id']
    print(venue_id)
    photo_params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "v": 20210201,
        'VENUE_ID' : venue_id,
        'limit' : 1
    }
    photo_results_json = requests.get(photo_url, params=photo_params).json()
    context = {   
        'results': results_json,
        'photos' : photo_results_json
    }
    print('----------------')
    pp.pprint(photo_results_json)
    print('---------------')
    return render_template('results.html', results=results_json, photos='photos')


if __name__ == '__main__':
    app.run(debug=True)
