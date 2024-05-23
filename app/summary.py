import requests
from transformers import pipeline

def get_video_id(url):
    import re
    pattern = r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

def get_subtitles(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/captions?videoId={video_id}&key={api_key}"
    response = requests.get(url)
    captions = response.json().get('items', [])
    if captions:
        caption_id = captions[0]['id']
        caption_url = f"https://www.googleapis.com/youtube/v3/captions/{caption_id}?key={api_key}&tfmt=srv3"
        response = requests.get(caption_url)
        return response.text
    return None

def summarize_text(text):
    summarizer = pipeline('summarization')
    return summarizer(text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
