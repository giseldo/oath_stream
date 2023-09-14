import streamlit as st
from streamlit_oauth import OAuth2Component
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials 

# Load environment variables from .env file
#from dotenv import load_dotenv
#load_dotenv()

AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"
CLIENT_ID = "80547735486-v27sr7scvtldgdagtj5gpf8ke2bquoph.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8501/component/streamlit_oauth.authorize_button/index.html"
SCOPE = "openid profile email https://www.googleapis.com/auth/classroom.courses.readonly"

# Set environment variables
#AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL')
#TOKEN_URL = os.environ.get('TOKEN_URL')
#REFRESH_TOKEN_URL = os.environ.get('REFRESH_TOKEN_URL')
#REVOKE_TOKEN_URL = os.environ.get('REVOKE_TOKEN_URL')
#CLIENT_ID = os.environ.get('CLIENT_ID')
#CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
#REDIRECT_URI = os.environ.get('REDIRECT_URI')
#SCOPE = os.environ.get('SCOPE')

# Create OAuth2Component instance
oauth2 = OAuth2Component(CLIENT_ID, CLIENT_SECRET, AUTHORIZE_URL, TOKEN_URL, REFRESH_TOKEN_URL, REVOKE_TOKEN_URL)

# Check if token exists in session state
if 'token' not in st.session_state:
    # If not, show authorize button
    result = oauth2.authorize_button("Authorize", REDIRECT_URI, SCOPE)
    
    if result and 'token' in result:
        # If authorization successful, save token in session state
        st.session_state.token = result.get('token')
        st.experimental_rerun()
else:
    # If token exists in session state, show the token
    token = st.session_state['token']
    st.write("Funcionou")
    st.json(token)
    access_token =token.get("access_token")
    st.write(access_token)
    creds = Credentials(token=access_token)
    
    #creds = AccessTokenCredentials(token=token)
    service = build('classroom', 'v1', credentials=creds)
    # Call the Classroom API
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    
    st.write('Courses:')
    for course in courses:
        st.write(course['name'])
        
    if st.button("Refresh Token"):
        # If refresh token button is clicked, refresh the token
        token = oauth2.refresh_token(token)
        st.session_state.token = token
        st.experimental_rerun()