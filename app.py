import os
import json
import pymongo
import subprocess

from flask import Flask, redirect, url_for
from flask_cors import CORS, cross_origin
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter

app = Flask(__name__)
app.secret_key = os.environ['SESSION_SECRET']
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app)
blueprint = make_twitter_blueprint(
    api_key=os.environ['API_KEY'],
    api_secret=os.environ['API_SECRET'],
)
app.register_blueprint(blueprint, url_prefix="/login")


@app.route("/", methods=["GET"])
@cross_origin()
def index():
    if not twitter.authorized:
        return redirect(url_for("twitter.login"))
    resp = twitter.get("statuses/user_timeline.json")
    assert resp.ok

    return json.dumps(resp.json())
