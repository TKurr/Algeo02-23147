import os
import json
from flask import send_from_directory, jsonify, request, Blueprint

# API Blueprint
mapper_api = Blueprint("mapper_api", __name__)

# Configuration paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAPPER_FILE = os.path.join(BASE_DIR, "../../test/dataset/mapper/mapper.json")
IMAGE_FOLDER = "src/backend/test/dataset/image_dataset"
AUDIO_FOLDER = "src/backend/test/dataset/audio_dataset"
PUBLIC_FOLDER = "src/frontend/public"

def load_mapper():
    """Load the mapper.json file."""
    with open(MAPPER_FILE, "r") as file:
        return json.load(file)

def get_image_by_audio(audio_file):
    """Fetch the corresponding image or return a default image."""
    mapper = load_mapper()
    for entry in mapper:
        if entry["audio_file"] == audio_file:
            image_name = entry["pic_name"]
            image_path = os.path.join(IMAGE_FOLDER, image_name)
            if os.path.isfile(image_path):
                return send_from_directory(IMAGE_FOLDER, image_name)
    
    # Return the fallback image
    fallback_image = "default.jpg"
    fallback_path = os.path.join(PUBLIC_FOLDER, fallback_image)
    if os.path.isfile(fallback_path):
        return send_from_directory(PUBLIC_FOLDER, fallback_image)
    return {"error": "Default image not found"}, 404

def get_image_by_image(image_file):
    """Fetch the corresponding image or return a default image."""
    mapper = load_mapper()
    for entry in mapper:
        if entry["pic_name"] == image_file:
            image_name = entry["pic_name"]
            image_path = os.path.join(IMAGE_FOLDER, image_name)
            if os.path.isfile(image_path):
                return send_from_directory(IMAGE_FOLDER, image_name)
    
    # Return the fallback image
    fallback_image = "default.jpg"
    fallback_path = os.path.join(PUBLIC_FOLDER, fallback_image)
    if os.path.isfile(fallback_path):
        return send_from_directory(PUBLIC_FOLDER, fallback_image)
    return {"error": "Default image not found"}, 404

def get_audio_by_image(image_file):
    """Fetch the corresponding image or return a default image."""
    mapper = load_mapper()
    for entry in mapper:
        if entry["pic_name"] == image_file:
            audio_name = entry["audio_file"]
            audio_path = os.path.join(AUDIO_FOLDER, audio_name)
            if os.path.isfile(audio_path):
                return send_from_directory(AUDIO_FOLDER, audio_name)
            
#Route: Fetch image based on audio_file
@mapper_api.route("/get-image", methods=["GET"])
def get_image():
    audio_file = request.args.get("audio_file")
    if not audio_file:
        return jsonify({"error": "audio_file parameter is required"}), 400
    return get_image_by_audio(audio_file)

@mapper_api.route("/get-image-image", methods=["GET"])
def get_image_image():
    image_file = request.args.get("image_file")
    if not image_file:
        return jsonify({"error": "image_file parameter is required"}), 400
    return get_image_by_audio(image_file)

@mapper_api.route("/get-audio", methods=["GET"])
def get_audio():
    image_file = request.args.get("image_file")
    if not image_file:
        return jsonify({"error": "image_file parameter is required"}), 400
    return get_audio_by_image(image_file)