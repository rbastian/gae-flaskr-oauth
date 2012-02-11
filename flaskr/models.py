__author__ = 'rbastian'


from google.appengine.ext import db

class Post(db.Model):
    screen_name = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
