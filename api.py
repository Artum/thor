import time
from flask import Flask, redirect, url_for, session, abort, request
from oauth2client import client


app = Flask(__name__)
app.secret_key = '7b57f060-169f-4c3f-a7a9-fa6592f12f58'
app.config.from_object('config')



@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/<path:path>', methods=['GET'])
def any_root_path(path):
    return render_template('index.html')

@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/api/authorize', methods=["POST"])
def login():
    """
    https://developers.google.com/identity/sign-in/web/server-side-flow#python
    """
    
    auth_code = request.get_json()["auth_code"]
    print(f"******** /api/authorize: auth_code = {auth_code}")
    if not request.headers.get('X-Requested-With'):
        abort(403)

    # Set path to the Web application client_secret_*.json file you downloaded from the
    # Google API Console: https://console.developers.google.com/apis/credentials
    CLIENT_SECRET_FILE = '/home/user/Desktop/dev/thor/client_secret.json'

    # Exchange auth code for access token, refresh token, and ID token
    credentials = client.credentials_from_clientsecrets_and_code(
        CLIENT_SECRET_FILE,
        ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
        auth_code)

    print(f"credentials = {credentials}")
    return "OK"
