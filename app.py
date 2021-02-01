from flask import Flask, request, redirect, render_template, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import MongoClient
from dotenv import load_dotenv
import os

#Setup

app = Flask(__name__)


#Flask routes

@app.route('/')
def home_page():
    '''Display homepage'''
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)