from flask import (
    request,
    redirect,
    render_template,
    url_for,
    Blueprint,
    session,
    flash
)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import PrettyPrinter
from operator import itemgetter
import datetime
import requests
import json
import os
from proxcity_app import bcrypt, mongo, app

##########################################
#                  Setup                 #
##########################################

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

pp = PrettyPrinter(indent=4)

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)


##########################################
#           Session Config               #
##########################################

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)
    session.modified = True


##########################################
#              Main Routes               #
##########################################

@main.route('/')
def home():
    '''Display homepage'''
    return render_template('home.html')


@main.route('/about')
def about():
    '''Display about page'''
    return render_template('about.html')


@main.route('/user', methods=["GET", "POST"])
def user():
    '''Display User Page'''
    if 'email' in session:
        user = mongo.db.users.find_one({'email': session['email']})

        if request.method == "GET":
            # Query the db for favorites and user data
            favorites = list(mongo.db.favorites.find({'user_id': user['_id']}))
            print(favorites)
            context = {
              'user': user,
              'favorites': favorites
            }
            return render_template('user.html', **context)
        else:
            # Add new favorite to user in db and display user page
            favorite = {
               'name': request.form.get("name"),
               'address': request.form.get('address'),
               'description': request.form.get('description'),
               'photo_path': request.form.get('photo_path'),
               'user_id': user['_id']
            }
            mongo.db.favorites.insert_one(favorite)

            return redirect(url_for('main.user'))
    else:
        return redirect(url_for('auth.login'))


@main.route('/results')
def results():
    '''Display result page'''
    query = request.args.get("search-query")
    city = request.args.get("city")
    zipcode = request.args.get("zipcode")
    if not zipcode:
        flash("Please enter a zipcode")
        return render_template('home.html')
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
        description_results = requests.get(
            description_url, params=desc_params).json()
        # pp.pprint(description_results)
        # Tries to get picture and description
        try:
            description = description_results['response']['venue'][
                'description']
        # Uses a placeholder if info does not exist
        except KeyError:
            description = "No Description Given"
        descriptions.append(description)
        try:
            photo = photo_prefix + description_results[
                'response']['venue']['bestPhoto']['suffix']
        except KeyError:
            photo = url_for('static', filename='Logo.png')
        photos.append(photo)

    context = {
        'results': results,
        'num_venues': len(results),
        'photos': photos,
        'desc': descriptions
    }
    return render_template('results.html', **context)


@main.route('/delete', methods=['POST'])
def delete():
    """remove favorite from user"""
    item = request.form.get('id')
    mongo.db.favorites.delete_one(
        {'_id': ObjectId(item)}
    )
    return redirect(url_for('main.user'))


##########################################
#             Auth Routes                #
##########################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    '''Display signup page'''
    if 'email' in session:
        return redirect(url_for('main.home'))

    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        email, name, password = itemgetter(
            'email', 'name', 'password')(request.form)

        # Form input sanitization
        if email is None or type(email) is not str or \
                name is None or type(name) is not str or \
                password is None or type(password) is not str:
            flash('ERROR: Form input is not in the correct format')
            return redirect(url_for('auth.signup'))

        # Check if the user already exists in the database, if so go to login
        user = mongo.db.users.find_one({'email': email})

        if user is not None:
            flash('ERROR: User already exists in the database.')
            return redirect(url_for('auth.login'))

        # Insert the user into the database
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        session['email'] = email

        new_user = {
            'email': email,
            'name': name,
            'password': hashed_password
        }

        mongo.db.users.insert_one(new_user)

        return redirect(url_for('main.home'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    '''Display login page'''
    if 'email' in session:
        return redirect(url_for('main.home'))

    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        email, password = itemgetter('email', 'password')(request.form)

        # Form input sanitization
        if (
            email is None or type(email) is not str or
            password is None or type(password) is not str
           ):
            flash('ERROR: Form input is not in the correct format')
            return redirect(url_for('auth.login'))

        user = mongo.db.users.find_one({'email': email})

        # If the user is not found in the database
        if user is None:
            flash('ERROR: User not found, please signup')
            return redirect(url_for('auth.signup'))

        # If the passwords do not match
        if not bcrypt.check_password_hash(user['password'], password):
            flash('ERROR: Password is incorrect')
            return redirect(url_for('auth.login'))

        session['email'] = email
        flash('Successfully logged in!')
        return redirect(url_for('main.home'))


@auth.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('auth.login'))
