import os
import json
import pymongo
import subprocess
import pandas as pd

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

    user_settings = twitter.get("account/settings.json")
    screen_name = user_settings.json()['screen_name']

    mclient = pymongo.MongoClient(os.environ['MONGO_CLIENT'])
    mdb = mclient[os.environ['DB_NAME']]
    count = mdb[screen_name].count()
    
    if count > 0:
        print('fetching from db')
        resp = list(mdb[screen_name].find({}, {'_id': 0}))
    else:
        print('fetching from api')
        resp = twitter.get("statuses/user_timeline.json")
        if not resp.ok:
            return {
                'statusCode': 500,
                'body': 'Internal server error'
            }
        resp = resp.json()
        _ = mdb[screen_name].insert_many(resp)

    df = pd.DataFrame(resp)
    df['created_at_dt'] = pd.to_datetime(df['created_at'])
    df.sort_values(by='created_at_dt', inplace=True)

    return df.to_html()
