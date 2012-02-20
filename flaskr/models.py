__author__ = 'rbastian'


from google.appengine.ext import db
from tweepy.oauth import OAuthToken



class User(db.Model):
    id = db.IntegerProperty(required=True)
    access_token = db.StringProperty(required = False)
    screen_name = db.StringProperty(required = True)
    created = db.DateTimeProperty(required = True, auto_now=False, auto_now_add=True)

class Post(db.Model):
    author = db.ReferenceProperty(reference_class=User, collection_name="posts")
    created = db.DateTimeProperty(required = True, auto_now=False, auto_now_add=True)
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

