__author__ = 'rbastian'

from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash
from flaskr import app
from models import Post
from google.appengine.api import users
from oauth import get_oauth_redirect, get_oauth_access_token, get_screen_name
import logging

logger = logging.getLogger()

@app.route('/')
def show_entries():

    posts = Post.all()
    return render_template('show_entries.html', entries=posts)

@app.route('/add', methods=['POST'])
def add_entry():

    if not session.get('logged_in'):
        abort(401)

    post = Post(screen_name = get_screen_name(), title=request.form['title'], content=request.form['text'])
    post.put()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/oauth_callback', methods=['GET'])
def oauth_callback():

    access_token = get_oauth_access_token(request.args['oauth_verifier'])
    if access_token:
        session['access_token'] = access_token
        session['logged_in'] = True
    else:
        flash("Twitter denied authorization request!")

    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET'])
def login():

    if not session.get('logged_in'):
        if not session.get('access_token'):
            return redirect(get_oauth_redirect())
        else:
            session['logged_in'] = True

    return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('access_token', None)
    flash('You were logged out')
    return redirect(users.create_logout_url(url_for('show_entries')))
