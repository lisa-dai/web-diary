"""
webdiary POSTS.

URLs include:
/diary/
"""
import sqlite3
import flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Return Index."""
    return flask.render_template('index.html')

@app.route('/submit/', methods=['POST'])
def handle_posts():
    """Handle Diary Posts."""

    # Connect to database
    conn = sqlite3.connect('var/webdiary.sqlite3')

    title = flask.request.form['title']
    text = flask.request.form['text']

    if not text:
        flask.abort(400)  # ERROR: text is empty
    else:
        # insert a new comment
        conn.execute("INSERT INTO posts (title, text)"
                    " VALUES (?, ?)",
                    (title, text))
        # need to commit changes after executing SQL command
        conn.commit()
    return flask.redirect('/diary/')

@app.route('/diary/', methods=['GET'])
def diary():
    """Render Diary Template."""

    conn = sqlite3.connect('var/webdiary.sqlite3')
    # returns post as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template('diary.html', posts=posts)

@app.route('/new-post/', methods=['GET'])
def newpost():
    """Return New Post."""
    return flask.render_template('new-post.html')
