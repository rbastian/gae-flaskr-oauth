__author__ = 'rbastian'


from flask import Flask
import settings

app = Flask('flaskr')
app.config.from_object('flaskr.settings')

import views