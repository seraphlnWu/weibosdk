# coding=utf8
import sys
import os
from os.path import realpath, dirname
from os.path import join as path_join
sys.path.insert(
    0,
    realpath(
        path_join(dirname(__file__), '../')
    )
)

import pymongo
from datetime import datetime
from time import time

from sinaapi import SinaAPI

db = pymongo.Connection('localhost')['sandbox_mongo_5']

APP_KEY = "1234567789"
APP_SECRET = "asdfjkalsdfjl"
CALLBACK_URL = 'http://www.example.com/callback/'

def get_api(uid):
    user_info = db.users.find_one({'_id': uid}, {'tok': 1, 'exp': 1})
    api = None
    if user_info.get('tok', 0):
        apiclient = SinaAPI(
            app_key=APP_KEY,
            app_secret=APP_SECRET,
            redirect_uri=CALLBACK_URL,
        )
        apiclient.set_access_token(user_info['tok'], str(user_info['exp']))
        api = apiclient
    else:
        pass

    return api
