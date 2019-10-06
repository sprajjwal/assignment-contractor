from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
playlists = db.playlists

db = client.get_default_database()
playlists = db.playlists
comments = db.comments

app = Flask(__name__)

@app.route('/')
def playlists_index():
    """Show all playlists."""
    return render_template('store_home.html', playlists=playlists.find())
