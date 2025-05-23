"""
webdiary POSTS.

URLs include:
/diary/
"""
import sqlite3
from datetime import datetime
import uuid
import hashlib
import flask
from flask import Blueprint, render_template, redirect, url_for, session, request, abort, jsonify

diary_bp = Blueprint('diary_bp', __name__)

@diary_bp.route('/', methods=['GET'])
def index():
    """Return Index."""
    return render_template('index.html')

@diary_bp.route('/diary/', methods=['GET'])
def diary():
    """Render Diary."""
    # not authorized to view diary
    if "authenticated" not in session:
        return render_template('diary.html', posts=None, authenticated=False)
    
    conn = sqlite3.connect('var/webdiary.sqlite3')
    # returns post as dictionaries instead of tuples
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM posts ORDER BY created DESC').fetchall()
    conn.close()
    return render_template('diary.html', posts=posts, authenticated=True)

@diary_bp.route('/validatepwd/', methods=['POST'])
def validate():
    """Validate Password to View Diary Posts."""

    # algorithm$salt$hash
    stored_pwd = 'sha512$210b91ab17c1490b8d66858497df60c0$1a9d624a7cf1ed3554969dd68c987e14d7fb790ddbe4c331aa032486fc0264487335f7ea942ed15bf5ec69e119f491be67fc41973f2bb3fc737b29092d22aee4'
    algorithm, salt, stored_hash = stored_pwd.split('$')

    input_pwd = request.form['pass']

    hash_obj = hashlib.new(algorithm)
    salted_pwd = salt + input_pwd
    # encodes salted pwd string into UTF-8 bytes, as hashing functions require bytes as input
    hash_obj.update(salted_pwd.encode('utf-8'))
    # computes the final SHA-512 hash of the salted password, returns as hexadecimal str
    input_hash = hash_obj.hexdigest()

    # correct pwd
    if input_hash == stored_hash:
        session['authenticated'] = True

    # incorrect pwd
    else:
        if request.form['url'] == '/diary/':
            return render_template('diary.html', posts=None, authenticated=False, alert='stop trying to read my diary >:(')
    
    return redirect(request.form['url'])

@diary_bp.route('/submit/', methods=['POST'])
def handle_posts():
    """Handle Diary Post Submits."""

    # connect to database
    conn = sqlite3.connect('var/webdiary.sqlite3')

    title = request.form['title']
    text = request.form['text']
    created = datetime.now().replace(microsecond=0)

    if not text:
        abort(400)  # ERROR: text is empty
    else:
        # insert new post
        conn.execute("INSERT INTO posts (title, text, created)"
                    " VALUES (?, ?, ?)",
                    (title, text, created))
        # need to commit changes after executing SQL command
        conn.commit()
    return redirect('/diary/')

@diary_bp.route('/new-post/', methods=['GET'])
def newpost():
    """Return New Diary Post Form."""
    if "authenticated" not in session:
        return render_template('new-post.html', authenticated=False)
    return render_template('new-post.html', authenticated=True)

'''@diary_bp.route('api/diary/<postid>', methods=['PATCH'])
def diaryedit(postid):
    """Edit Diary Entry."""
    if "authenticated" not in session:
        return render_template('diary.html', posts=None, authenticated=False)
    data = request.get_json()
    title = data.get('title')
    text = data.get('text')

    conn = sqlite3.connect('var/webdiary.sqlite3')
    conn.row_factory = sqlite3.Row

    conn.execute("UPDATE posts SET title=?, text=? WHERE postid=?",
                 (title, text, postid,))
    conn.commit()
    return flask.jsonify()'''


@diary_bp.route('/diarydelete/', methods=['POST'])
def diarydelete():
    """Delete Diary Entry."""

    conn = sqlite3.connect('var/webdiary.sqlite3')
    conn.row_factory = sqlite3.Row

    postid = request.form['postid']
    conn.execute("DELETE FROM posts WHERE postid=?",
                 (postid,))
    conn.commit()
    return redirect('/diary/')
