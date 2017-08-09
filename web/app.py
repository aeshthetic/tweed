"""Entry point for flask application"""
import json
import os
from random import shuffle
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
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
    """Displays a feed of content from instagram and twitter"""
    scrape_data()
    with open(os.path.join(REFERENCE_DIR, "profile_spider.json"), "r") as f:
        twimages = json.load(f)

    status = tweets()
    twimages.extend(t for t in tweets())
    shuffle(twimages)

    return render_template('feed.html', twimages=twimages, status=status)


if __name__ == '__main__':
    app.run()
