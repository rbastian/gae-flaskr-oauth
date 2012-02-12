__author__ = 'rbastian'

from tweepy import OAuthHandler
from tweepy import TweepError
from tweepy import API

import settings_local
import logging

consumer_key = settings_local.consumer_key
consumer_secret = settings_local.consumer_secret
auth = OAuthHandler(consumer_key, consumer_secret, callback='http://localhost:8080/oauth_callback')
logger = logging.getLogger()

def get_oauth_redirect():

    try:
        redirect_url = auth.get_authorization_url()
    except TweepError as e:
        logger.error("Failed to get request token: %s", e)

    return redirect_url

def get_oauth_access_token(verifier):

    try:
        auth.get_access_token(verifier)
        logger.info('successful conversion of request token to auth_token: %s', auth.access_token)
    except TweepError as e:
        logger.error('Caught TweepError: %s, while trying to get access_token')

    return auth.access_token

def get_screen_name():
    return auth.get_username()

def get_user():
    api = API(auth_handler = auth)
    return api.me()
