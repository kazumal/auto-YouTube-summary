from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['YOUTUBE_API_KEY'] = os.getenv('YOUTUBE_API_KEY')

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
