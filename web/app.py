import json
import os
from random import shuffle
from flask import Flask, request, render_template, flash, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import BaseConfig
from util import scrape_data, REFERENCE_DIR, tweets

app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)

from models import *

@app.route('/')
def index():
    """Returns index page"""
    return render_template('index.html')

@app.route('/feed')
def feed():
    scrape_data()
    with open(os.path.join(REFERENCE_DIR, "profile_spider.json"), "r") as f:
        twimages = json.load(f)
    
    status = tweets()
    for tweet in status:
        twimages.append(tweet)
    shuffle(twimages)

    return render_template('feed.html', twimages=twimages, status=status)

if __name__ == '__main__':
    app.run()
