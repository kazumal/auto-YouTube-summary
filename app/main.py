from flask import Blueprint, request, jsonify, render_template, current_app
from .summary import get_video_id, get_subtitles, summarize_text

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/summary', methods=['POST'])
def summary():
    data = request.get_json()
    url = data['url']
    api_key = current_app.config['YOUTUBE_API_KEY']
    video_id = get_video_id(url)
    subtitles = get_subtitles(video_id, api_key)
    if subtitles:
        summary = summarize_text(subtitles)
        return jsonify({'summary': summary})
    return jsonify({'summary': 'No subtitles available'})
