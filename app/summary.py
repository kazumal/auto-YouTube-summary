import os
import requests
import json
from transformers import pipeline
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# 環境変数からOAuth 2.0の認証情報を取得
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
PROJECT_ID = os.getenv('PROJECT_ID')

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def get_video_id(url):
    import re
    pattern = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_authenticated_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_config = {
                "installed": {
                    "client_id": CLIENT_ID,
                    "project_id": PROJECT_ID,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_secret": CLIENT_SECRET,
                    "redirect_uris": ["http://localhost"]
                }
            }
            flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_subtitles(video_id):
    creds = get_authenticated_service()
    url = f"https://www.googleapis.com/youtube/v3/captions?videoId={video_id}"
    headers = {
        'Authorization': f'Bearer {creds.token}',
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers)
    print("API response status:", response.status_code)
    print("API response content:", response.json())
    captions = response.json().get('items', [])
    if captions:
        caption_id = captions[0]['id']
        caption_url = f"https://www.googleapis.com/youtube/v3/captions/{caption_id}?tfmt=srv3"
        response = requests.get(caption_url, headers=headers)
        return response.text
    return None

def summarize_text(text):
    summarizer = pipeline('summarization', model="facebook/bart-large-cnn")
    return summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
