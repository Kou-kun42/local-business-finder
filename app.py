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
def home():
    '''Display homepage'''
    return render_template('home.html')

@app.route('/results')
def results():
  "Display result cards"
  return render_template('results.html')

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


if __name__ == '__main__':
    app.run(debug=True)
