__author__ = 'rbastian'

from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash
from flaskr import app
from models import Post, User
from oauth import get_oauth_redirect, get_oauth_access_token, get_screen_name, get_user, update_status
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
    user = session.get('user')
    post = Post(author=user, title=request.form['title'], content=request.form['text'])
    post.put()
    logger.info('request.form = %s', request.form)
    key = 'tweetthis'
    if key in request.form:
        update_status(status = request.form['title'])
    return redirect(url_for('show_entries'))

@app.route('/oauth_callback', methods=['GET'])
def oauth_callback():

    access_token = get_oauth_access_token(request.args['oauth_verifier'])
    if access_token:
        session['logged_in'] = True
        flash('Logged in as %s' % get_screen_name())
        user = User.get_by_key_name(get_screen_name())
        if not user:
            user = User(key_name = get_screen_name(), access_token = access_token.to_string(), screen_name = get_screen_name(), id = get_user().id)
        session['user'] = user
        user.put()
    else:
        flash("Twitter denied authorization request!")

    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET'])
def login():

    if not session.get('logged_in'):
        return redirect(get_oauth_redirect())

    return redirect(url_for('show_entries'))

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
