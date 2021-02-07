from apiclient import discovery
import httplib2
from oauth2client import client

# (Receive auth_code by HTTPS POST)


# If this request does not have `X-Requested-With` header, this could be a CSRF
if not request.headers.get('X-Requested-With'):
    abort(403)

# Set path to the Web application client_secret_*.json file you downloaded from the
# Google API Console: https://console.developers.google.com/apis/credentials
CLIENT_SECRET_FILE = '/path/to/client_secret.json'

# Exchange auth code for access token, refresh token, and ID token
credentials = client.credentials_from_clientsecrets_and_code(
    CLIENT_SECRET_FILE,
    ['https://www.googleapis.com/auth/drive.appdata', 'profile', 'email'],
    auth_code)

# Call Google API
http_auth = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http_auth)
appfolder = drive_service.files().get(fileId='appfolder').execute()

# Get profile info from ID token
userid = credentials.id_token['sub']
email = credentials.id_token['email']

# try:
#   from flask import (
#       Flask,
#       flash,
#       redirect,
#       render_template_string,
#       request,
#       session,
#       url_for,
#     )
    
#   import requests
#   from requests_oauthlib import OAuth2Session

# except ImportError:
#     raise RuntimeError('Requirements not set up, see "Requirements":\n' + __doc__)
  
# from flask import current_app as app

# @app.route('/auth', defaults={'action': 'login'})
# @app.route('/auth/<action>')
# def auth(action):
#     """ All-purpose authentication view.
#         Stores `next` GET param in session (to persist around OAuth redirects)
#         Stores referrer in session (to redirect back to on error)
#         Refreshes token for logged in user if action == 'refresh'
#         Revokes the token for logged in user if action == 'revoke'
#         Logs out already logged-in users if action == 'logout'
#         Handles initial redirect off to Google to being OAuth 2.0 flow
#         Handles redirect back from Google & retreiving OAuth token
#         Stores user info & OAuth token in `session['user']`
#     """

#     # Store some useful destinations in session
#     if not request.args.get('state'):
#         session['last'] = request.referrer or url_for('index')
#         if 'next' in request.args:
#             session['next'] = url_for(request.args['next'])
#         else:
#             session['next'] = session['last']

#     # User logged in, refresh
#     if session.get('user') and action == 'refresh':
#         if 'refresh_token' not in session['user']['token']:
#             flash('Could not refresh, token not present', 'danger')
#             return redirect(session['last'])
#         google = OAuth2Session(
#           app.config['GOOGLE_CLIENT_ID'],
#           token=session['user']['token']
#         )
#         session['user']['token'] = google.refresh_token(
#           'https://accounts.google.com/o/oauth2/token',
#           client_id=app.config['GOOGLE_CLIENT_ID'],
#           client_secret=app.config['GOOGLE_CLIENT_SECRET']
#         )
#         flash('Token refreshed', 'success')
#         return redirect(session['next'])

#     # User loggedin - logout &/or revoke
#     if session.get('user'):
#         if action == 'revoke':
#             response = requests.get(
#               'https://accounts.google.com/o/oauth2/revoke',
#               params={'token': session['user']['token']['access_token']}
#             )
#             if response.status_code == 200:
#                 flash('Authorization revoked', 'warning')
#             else:
#                 flash('Could not revoke token: {}'.format(response.content), 'danger')
#         if action in ['logout', 'revoke']:
#             del session['user']
#             flash('Logged out', 'success')
#         return redirect(session['last'])

#     google = OAuth2Session(
#       app.config['GOOGLE_CLIENT_ID'],
#       scope=[
#         'https://www.googleapis.com/auth/userinfo.email',
#         'https://www.googleapis.com/auth/userinfo.profile',
#       ],
#       redirect_uri=url_for('auth', _external=True),
#       state=session.get('state')
#     )

#     # Initial client request, no `state` from OAuth redirect
#     if not request.args.get('state'):
#         url, state = google.authorization_url(
#           'https://accounts.google.com/o/oauth2/auth',
#           access_type='offline'
#         )
#         session['state'] = state
#         return redirect(url)

#     # Error returned from Google
#     if request.args.get('error'):
#         error = request.args['error']
#         if error == 'access_denied':
#             error = 'Not logged in'
#         flash('Error: {}'.format(error), 'danger')
#         return redirect(session['last'])

#     # Redirect from google with OAuth2 state
#     token = google.fetch_token(
#       'https://accounts.google.com/o/oauth2/token',
#       client_secret=app.config['GOOGLE_CLIENT_SECRET'],
#       authorization_response=request.url
#     )
#     user = google.get('https://www.googleapis.com/oauth2/v1/userinfo').json()
#     user['token'] = token
#     session['user'] = user
#     flash('Logged in', 'success')
#     return redirect(session['next'])

# import google.oauth2.credentials
# import google_auth_oauthlib.flow 
# from flask_session import Session

# from flask import current_app as app

# # for server side sessions
# ## Commenting these two lines allows everything to work
# app.config['SESSION_TYPE'] = 'filesystem'
# Session(app)


# GOOGLE_OAUTH2_CLIENT_ID =     app.config['GOOGLE_CLIENT_ID'],
# GOOGLE_OAUTH2_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']
# REDIRECT_URI = '/oauth2callback'


# CLIENT_CONFIG = {'web':{
#     'client_id':GOOGLE_OAUTH2_CLIENT_ID ,
#     'client_secret':GOOGLE_OAUTH2_CLIENT_SECRET,
#     'redirect_uris':["http://localhost:5000/oauth2callback"],
#     'auth_uri':"https://accounts.google.com/o/oauth2/auth",
#     'token_uri':"https://accounts.google.com/o/oauth2/token"
#     }}

# SCOPES=["https://www.googleapis.com/auth/userinfo.profile","https://www.googleapis.com/auth/userinfo.email"]

# def generate_csrf_token():
#     if '_csrf_token' not in session:
#         session['_csrf_token'] = some_random_string()
#     return session['_csrf_token']


# def check_access_token():
#     return 'credentials' in session

# @app.route('/login')
# def login():
#     flow = google_auth_oauthlib.flow.Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES)
#     flow.redirect_uri = url_for('oauth2callback', _external=True)
#     authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
#     session['state'] = state
#     return redirect(authorization_url)


# def credentials_to_dict(credentials):
#     return {'token': credentials.token,
#             'refresh_token': credentials.refresh_token,
#             'token_uri': credentials.token_uri,
#             'client_id': credentials.client_id,
#             'client_secret': credentials.client_secret,
#             'scopes': credentials.scopes}

# @app.route('/oauth2callback')
# def oauth2callback():
#     state = session.get('state')
#     flow = google_auth_oauthlib.flow.Flow.from_client_config(CLIENT_CONFIG, scopes=SCOPES, state=state)
#     flow.redirect_uri = url_for('oauth2callback', _external=True)
#     authorization_response = request.url
#     flow.fetch_token(authorization_response=authorization_response)
#     credentials = flow.credentials
#     id_info = jwt.decode(credentials.id_token, verify=False)
#     email = id_info['email']
#     #allow anyone from example.com to log in 
#     if email.split('@')[1] != "example.com":
#         return "Login failed!"
#     session['credentials'] = credentials_to_dict(credentials)
#     session.modified = True
#     #return render_template()
#     return redirect(url_for('loglist'))

# @app.route("/")
# @app.route("/loglist")
# def loglist():
#     if not check_access_token():
#         return redirect(url_for('login'))
#     return "yay!"