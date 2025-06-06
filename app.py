import os
from flask import Flask
from webdiary import diary_bp
from art import art_bp

app = Flask(__name__)
app.secret_key = os.urandom(64)

# Register blueprints
app.register_blueprint(diary_bp)
app.register_blueprint(art_bp)

if __name__ == '__main__':
    app.run(debug=True)
