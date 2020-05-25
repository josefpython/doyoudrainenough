import os
import spotipy
import spotipy.util as util
import sys
from flask import Flask, redirect, url_for

app = Flask(__name__)
#SPOTIPY VARS
scope = 'user-library-read'
SPOTIPY_CLIENT_ID = '4fdb5917f07642b09c55c68caa96b4eb'
SPOTIPY_CLIENT_SECRET = '76a2d5a204734939b3cbe604af65ab70'
SPOTIPY_REDIRECT_URL = "http://127.0.0.1:9090/"
#SPOTIPY_REDIRECT_URL = "http://josefvongaming.pythonanywhere.com/code/"
username = sys.argv[0]

@app.route("/")
def main():
    return '<a href = "/login/"> Login </a> or <a href = "/results/"> Results </a> '

@app.route("/login/")
def login():
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URL)
    f = open("cache.txt", "w+")
    f.write(token)
    f.close()
    return redirect(url_for("main"))

@app.route("/results/")
def results():
    f = open("cache.txt", "r")
    token = f.read()
    f.close()
    os.remove("cache.txt")
    
    sp = spotipy.Spotify(auth=token)
    return sp.current_user_saved_tracks(limit=1)
