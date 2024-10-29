"""
webdiary POSTS.

URLs include:
/diary/
"""
import sqlite3
from datetime import datetime
import flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Return Index."""
    return flask.render_template('index.html')

@app.route('/art/', methods=['GET'])
def art():
    """Render Art."""
    return render_template('art.html')

@app.route('/submit/', methods=['POST'])
def handle_posts():
    """Handle Diary Posts."""

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

@app.route('/artsubmit/', methods=['POST'])
def handle_art():
    """Handle Art Posts."""

    # Connect to database
    conn = sqlite3.connect('var/webdiary.sqlite3')

    title = flask.request.form['title']
    text = flask.request.form['text']
    created = datetime.now().replace(microsecond=0)

    # Handle the file upload
    if 'filename' not in flask.request.files:
        flask.abort(400)  # ERROR: No file part
    file = flask.request.files['filename']
    
    if file.filename == '':
        flask.abort(400)  # ERROR: No selected file
    else:
        # insert new art
        conn.execute("INSERT INTO art (filename, title, text, created)"
                    " VALUES (?, ?, ?)",
                    (file.filename, title, text, created))
        # need to commit changes after executing SQL command
        conn.commit()
    return flask.redirect('/art/')

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
    """Return New Diary Post."""
    return flask.render_template('new-post.html')

@app.route('/new-art/', methods=['GET'])
def newart():
    """Render New Art Post."""
    return render_template('new-art.html')

@app.route('/artdelete/', methods=['POST'])
def artdelete():
    """Delete Art Entry."""

    conn = sqlite3.connect('var/webdiary.sqlite3')
    conn.row_factory = sqlite3.Row

    artid = flask.request.form['artid']
    conn.execute("DELETE FROM art WHERE artid=?",
                 (artid,))
    conn.commit()
    return flask.redirect('/art/')
