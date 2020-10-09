import tekore as tk
from flask import Flask, request, redirect, session, url_for, render_template
from ast import literal_eval

#SPOTIFY AUTHENTICATION PROCESSES

SPOTIPY_CLIENT_ID = '4fdb5917f07642b09c55c68caa96b4eb'
SPOTIPY_CLIENT_SECRET = '76a2d5a204734939b3cbe604af65ab70'
#SPOTIPY_REDIRECT_URL = "http://localhost:5000/callback"
SPOTIPY_REDIRECT_URL = "https://doyoudrainenough.herokuapp.com/callback"

conf = (SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URL)

cred = tk.Credentials(*conf)
spotify = tk.Spotify()

users = {}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cum'

@app.route('/', methods=['GET'])
def main():
    user = session.get('user', None)

    if user is not None:
        return redirect(url_for('results'))
    else:
        return render_template("index.html")

@app.route("/errorcatch/", methods=["GET"])
def error():
    #TODO Error catch and log
    return redirect(url_for("main"))


@app.route('/login/', methods=['GET'])
def login():
    auth_url = cred.user_authorisation_url(scope=tk.scope.every)
    return redirect(auth_url, 307)

@app.route('/callback/', methods=['GET'])
def login_callback():
    code = request.args.get('code', None)

    token = cred.request_user_token(code)
    with spotify.token_as(token):
        info = spotify.current_user()

    session['user'] = info.id
    users[info.id] = token

    return redirect('/', 307)

@app.route('/logout/', methods=['GET'])
def logout():
    uid = session.pop('user', None)
    if uid is not None:
        users.pop(uid, None)
    return redirect('/', 307)

#RESULTS PAGE

@app.route("/results/", methods=['GET'])
def results():

    draingang = ["2xvtxDNInKDV4AvGmjw6d1", "6hG0VsXXlD10l60TqiIHIX", "3cGojc1Yu89IHXx8OeSnee"]

    draincounter = 0
    offsetcounter = 0
    totalcounter = 0
    user = session.get('user', None)
    try:
        with spotify.token_as(users[user]):

            #score from saved tracks

            while True:
                reset = 0
                tracklist = spotify.saved_tracks(limit=50, offset=offsetcounter)

                for item in tracklist.items:
                    reset += 1
                    totalcounter += 1
                    artist = item.track.artists[0].id

                    if artist in draingang:
                        draincounter += 1

                if reset < 50:
                    break
                else:
                    offsetcounter += 50

            score_saved = draincounter/totalcounter*100
            if score_saved > 10:
                score_saved = 10

            #score from recent fav artists

            fvshort = 0
            score_fav_short = 0

            favartists_short = spotify.current_user_top_artists(time_range="short_term", limit=50)
            for item in favartists_short.items:
           
                if item.id in draingang:
                    score_fav_short = (score_fav_short + (100 - fvshort)) / 15

                fvshort += 2

            #score from midterm fav artists

            fvmid = 0
            score_fav_mid = 0

            favartists_mid = spotify.current_user_top_artists(time_range="medium_term", limit=50)
            for item in favartists_mid.items:
             
                if item.id in draingang:
                    score_fav_mid = (score_fav_mid + (100 - fvmid)) / 15 #CHANGE


                fvmid += 2

            #score from longterm fav artists

            fvlong = 0
            score_fav_long = 0
            dg_fav = []

            favartists_long = spotify.current_user_top_artists(time_range="long_term", limit=50)
            for item in favartists_long.items:
    
                if item.id in draingang:
                    score_fav_long = (score_fav_long + (100 - fvlong)) / 15
                    dg_fav.append(item.id)

                fvlong += 2

            #fav GTB track long term
        
            fav_tracks = spotify.current_user_top_tracks(time_range="long_term", limit=50)
            for item in fav_tracks.items:              
                if item.artists[0].id in draingang:
                    ft_name = item.name
                    ft_art = item.album.images[0].url
                    break

            if not ft_name:
                ft_name = 'None <p style="font-size: 15px; margin-top: 5px;"> You lackin bruh </p>'
                ft_art = "https://emojigraph.org/media/apple/pleading-face_1f97a.png"

            if score_fav_short > 10:
                score_fav_short = 10

            if score_fav_mid > 10:
                score_fav_mid = 10

            if score_fav_long > 10:
                score_fav_long = 10

            score = round( ((score_saved + score_fav_short + score_fav_mid + score_fav_long) / 4)*100 ) / 100

            if score < 2.5:
                bgc = "linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(255,0,0,1) 100%); color: white;"
            else:
                if score >= 5:
                    bgc = "background: linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(8,88,0,1) 100%);"
                else:
                    bgc = "linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(255,179,0,1) 100%); color: black;"
           

            try:
                fv_artist = spotify.artist(dg_fav[0])
                fav_a_img = literal_eval(str(fv_artist.images[2])).get("url")
                fav_a_name = str(fv_artist.name)
            except Exception:
                fav_a_img = "https://emojigraph.org/media/apple/pleading-face_1f97a.png"
                fav_a_name = 'Noone <p style="font-size: 15px; margin-top: 5px;"> Better go and listen to some drain! </p>'
                bgc = "linear-gradient(90deg, rgba(255,255,255,1) 0%, rgba(255,179,0,1) 100%); color: black;"
            

            return render_template("results.html", score=score, bgc=bgc, fav_a_img=fav_a_img, fav_a_name=fav_a_name, ft_img=ft_art, ft_name=ft_name)

    except KeyError:
        uid = session.pop('user', None)
        if uid is not None:
            users.pop(uid, None)
        return redirect(url_for('error'))

#if __name__ == "__main__":
#    app.run()

    
