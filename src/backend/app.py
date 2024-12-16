from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os

from feature.album_picture_finder.api_image_retrieval import image_api
from feature.data_upload.api_data_upload import upload_api
from feature.music_information_retrieval.api_music_retrieval import music_api
from feature.mapper_api.api_mapper import mapper_api

app = Flask(__name__)
CORS(app)

# Define the path to the MIDI dataset folder
MIDI_DATASET_FOLDER = os.path.abspath("test/dataset/midi_dataset")

# Register the Blueprint
app.register_blueprint(music_api, url_prefix='/')
app.register_blueprint(image_api, url_prefix='/')
app.register_blueprint(upload_api, url_prefix="/")
app.register_blueprint(mapper_api, url_prefix="/")

@app.route("/get_midi/<filename>", methods=["GET"])
def get_midi(filename):
    try:
        # Ensure only valid files are served
        if filename.endswith(".mid") or filename.endswith(".midi"):
            return send_from_directory(MIDI_DATASET_FOLDER, filename)
        else:
            return jsonify({"error": "Invalid file type"}), 400
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
