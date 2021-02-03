from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Setup

app = Flask(__name__)


# Flask routes

@app.route('/')
def home_page():
    '''Display homepage'''
    return render_template('home.html')


@app.route('/about')
def home_page():
    '''Display about page'''
    return render_template('about.html')


@app.route('/login')
def home_page():
    '''Display login page'''
    return render_template('login.html')


@app.route('/signup')
def home_page():
    '''Display signup page'''
    return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)
