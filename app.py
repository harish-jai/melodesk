from flask import Flask, redirect, url_for, session, request, jsonify
import spotipy
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.environ.get('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.environ.get('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URL = os.environ.get('SPOTIPY_REDIRECT_URL')

# Spotipy object to handle API calls
sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope='user-library-read'
))

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/login')
def login():
    auth_url = sp.auth_manager.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    session.clear()
    code = request.args.get('code')
    token_info = sp.auth_manager.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('get_playlists'))

@app.route('/playlists')
def get_playlists():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))
    sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope='user-library-read',
        token_info=token_info
    ))
    playlists = sp.current_user_playlists()
    return jsonify(playlists)

if __name__ == '__main__':
    app.run(debug=True)
