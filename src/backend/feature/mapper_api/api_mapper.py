import os
import json
from flask import send_from_directory, jsonify, request, Blueprint

# API Blueprint
mapper_api = Blueprint("mapper_api", __name__)

# Configuration paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MAPPER_FILE = os.path.join(BASE_DIR, "../../test/dataset/mapper/mapper.json")
IMAGE_FOLDER = os.path.join(BASE_DIR,"../../test/dataset/image_dataset")
AUDIO_FOLDER = os.path.join(BASE_DIR,"../../test/dataset/audio_dataset")
PUBLIC_FOLDER = os.path.join(BASE_DIR,"../../public")

def load_mapper():
    """Load the mapper.json file."""
    with open(MAPPER_FILE, "r") as file:
        return json.load(file)

def get_image_by_audio(audio_file):
    """Fetch the corresponding image or return an error if not found."""
    mapper = load_mapper()
    for entry in mapper:
        if entry["audio_file"] == audio_file:
            image_name = entry["pic_name"]
            image_path = os.path.join(IMAGE_FOLDER, image_name)
            if os.path.isfile(image_path):
                return send_from_directory(IMAGE_FOLDER, image_name)
    
    # If no matching image is found
    return {"error": "Image not found for the provided audio file"}, 404


def get_image_by_image(image_file):
    """Fetch the corresponding image or return a default image."""
    mapper = load_mapper()
    for entry in mapper:
        if entry["pic_name"] == image_file:
            image_name = entry["pic_name"]
            image_path = os.path.join(IMAGE_FOLDER, image_name)
            if os.path.isfile(image_path):
                return send_from_directory(IMAGE_FOLDER, image_name)
            
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
            
def get_all():
    """Return all the entries from the mapper."""
    mapper = load_mapper()
    new_map = []
    for entry in mapper:
        new_entry = {
            "file_name": entry["audio_file"],
            "similarity": 0,
            "image": entry["pic_name"]
        }
        new_map.append(new_entry)
    return new_map
            
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
    return get_image_by_image(image_file)

@mapper_api.route("/get-audio", methods=["GET"])
def get_audio():
    image_file = request.args.get("image_file")
    if not image_file:
        return jsonify({"error": "image_file parameter is required"}), 400
    return get_audio_by_image(image_file)

@mapper_api.route("/get-all", methods=["GET"])
def get_all_entries():
    try:
        data = get_all()
        return jsonify({"results": data}), 200  # Wrap the list in a JSON object
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle potential errors gracefully