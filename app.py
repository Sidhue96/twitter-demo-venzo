import os
import json
import pytz
import pymongo
import subprocess
import pandas as pd

from datetime import datetime
from flask import Flask, redirect, url_for, request
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
    print(screen_name)
    mclient = pymongo.MongoClient(os.environ['MONGO_CLIENT'])
    mdb = mclient[os.environ['DB_NAME']]
    count = mdb[screen_name].count()
    print(count)
    exceptions = []
    start_date, end_date = None, None

    if 'start' in request.args:
        try:
            start_date = datetime.strptime(request.args['start'], "%Y-%m-%d %H:%M:%S")
            start_date = pytz.utc.localize(start_date)

        except Exception as e:
            exceptions.append({
                'exception': str(e),
                'body': 'unable to filter based on start date'
            })
    
    if 'end' in request.args:
        try:
            end_date = datetime.strptime(request.args['end'], "%Y-%m-%d %H:%M:%S")
            end_date = pytz.utc.localize(end_date)

        except Exception as e:
            exceptions.append({
                'exception': str(e),
                'body': 'unable to filter based on end date'
            })
        
    to_find = {}
    if start_date is not None and end_date is not None:
        to_find['created_at_dt'] = {
            '$gte': start_date,
            '$lte': end_date
        }
    elif start_date is not None:
        to_find['created_at_dt'] = {
            '$gte': start_date
        }
    elif end_date is not None:
        to_find['created_at_dt'] = {
            '$lte': start_date
        }
    
    print(to_find)
    
    if count == 0:
        resp = twitter.get("statuses/user_timeline.json")
        if not resp.ok:
            return {
                'statusCode': 500,
                'body': 'Internal server error'
            }
        resp = resp.json()
        df = pd.DataFrame(resp)
        df['created_at_dt'] = pd.to_datetime(df['created_at'])
        _ = mdb[screen_name].insert_many(df.to_dict('records'))

    resp = list(mdb[screen_name].find(to_find, {'_id': 0}))

    asc = True
    if 'sort' in request.args and request.args['sort'] == 'desc':
        asc = False

    df = pd.DataFrame(resp)
    df.sort_values(by='created_at_dt', inplace=True, ascending=asc)
    # todo convert as api with exceptions

    # return df.drop('created_at_dt', axis=1).to_dict('records')
    return df.to_html()
