from flask import Flask
import os

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path=os.path.realpath('static'))


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/img.png')
def img():
    return app.send_static_file('img.png')
