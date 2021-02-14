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
    # Parameters for the venues api
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "query": query,
        "near": location,
        "v": 20210201,
        "limit": 4
    }
    
    results_json = requests.get(url, params=params).json()
    results = results_json['response']['venues']

    # Gets venue ids for additional info
    venue_ids = []
    for venue in results_json['response']['venues']:
        venue_ids.append(venue['id'])

    desc_params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "v": 20210201
    }

    # Gets picture and description of each location
    descriptions = []
    photos = []
    photo_prefix = 'https://fastly.4sqi.net/img/general/300x300'
    for venue_id in venue_ids:
        description_url = f"https://api.foursquare.com/v2/venues/{venue_id}"
        description_results = requests.get(description_url, params=desc_params).json()
        pp.pprint(description_results)
        # Tries to get picture and description
        try:
            description = description_results['response']['venue']['description']
        # Uses a placeholder if info does not exist
        except:
            description = "No Description Given"
        descriptions.append(description)
        try:
            photo = photo_prefix + description_results['response']['venue']['bestPhoto']['suffix']
        except:
            photo = url_for('static', filename='Logo.png')
        photos.append(photo)

    
    context = {   
        'results': results,
        'num_venues': len(results),
        'photos': photos,
        'desc': descriptions
    }
    return render_template('results.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
