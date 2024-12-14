from flask import Flask
from flask_cors import CORS
# from feature.album_picture_finder.api_image_retrieval import image_api
from feature.music_information_retrieval.api_music_retrieval import music_api

app = Flask(__name__)
CORS(app)

# Register the Blueprint
app.register_blueprint(music_api, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)
