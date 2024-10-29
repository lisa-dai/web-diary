"""
webdiary POSTS.

URLs include:
/diary/
"""
import sqlite3
from datetime import datetime
import flask
from flask import Blueprint, render_template

diary_bp = Blueprint('diary_bp', __name__)

@diary_bp.route('/', methods=['GET'])
def index():
    """Return Index."""
    return flask.render_template('index.html')

@diary_bp.route('/diary/', methods=['GET'])
def diary():
    """Render Diary."""

    conn = sqlite3.connect('var/webdiary.sqlite3')
    # returns post as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template('diary.html', posts=posts)

@diary_bp.route('/submit/', methods=['POST'])
def handle_posts():
    """Handle Diary Post Submits."""

    # Connect to database
    conn = sqlite3.connect('var/webdiary.sqlite3')

    title = flask.request.form['title']
    text = flask.request.form['text']
    created = datetime.now().replace(microsecond=0)

    if not text:
        flask.abort(400)  # ERROR: text is empty
    else:
        # insert new post
        conn.execute("INSERT INTO posts (title, text, created)"
                    " VALUES (?, ?, ?)",
                    (title, text, created))
        # need to commit changes after executing SQL command
        conn.commit()
    return flask.redirect('/diary/')

@diary_bp.route('/new-post/', methods=['GET'])
def newpost():
    """Return New Diary Post Form."""
    return flask.render_template('new-post.html')

@diary_bp.route('/diarydelete/', methods=['POST'])
def diarydelete():
    """Delete Diary Entry."""

    conn = sqlite3.connect('var/webdiary.sqlite3')
    conn.row_factory = sqlite3.Row

    postid = flask.request.form['postid']
    conn.execute("DELETE FROM posts WHERE postid=?",
                 (postid,))
    conn.commit()
    return flask.redirect('/diary/')
