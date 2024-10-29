"""
art POSTS.

URLs include:
/diary/
"""
import sqlite3
from datetime import datetime
import flask
import os
from flask import Blueprint, render_template

art_bp = Blueprint('art_bp', __name__)

@art_bp.route('/art/', methods=['GET'])
def art():
    """Render Art."""
    conn = sqlite3.connect('var/webdiary.sqlite3')
    conn.row_factory = sqlite3.Row

    arts = conn.execute('SELECT * FROM art ORDER BY created DESC').fetchall()
    conn.close()
    return render_template('art.html', arts=arts)

@art_bp.route('/artsubmit/', methods=['POST'])
def handle_art():
    """Handle Art Post Submits."""
    # Connect to database
    conn = sqlite3.connect('var/webdiary.sqlite3')

    file = flask.request.files['filename']
    title = flask.request.form['title']
    text = flask.request.form['text']
    created = datetime.now().replace(microsecond=0)

    # insert new art
    conn.execute("INSERT INTO art (filename, title, text, created)"
                " VALUES (?, ?, ?, ?)",
                (file.filename, title, text, created))
    file_path = os.path.join('static/images', file.filename)
    file.save(file_path)
    # need to commit changes after executing SQL command
    conn.commit()
    return flask.redirect('/art/')

@art_bp.route('/new-art/', methods=['GET'])
def newart():
    """Render New Art Post Form."""
    return render_template('new-art.html')

@art_bp.route('/artdelete/', methods=['POST'])
def artdelete():
    """Delete Art Entry."""

    conn = sqlite3.connect('var/webdiary.sqlite3')
    conn.row_factory = sqlite3.Row

    artid = flask.request.form['artid']
    conn.execute("DELETE FROM art WHERE artid=?",
                 (artid,))
    conn.commit()
    return flask.redirect('/art/')
