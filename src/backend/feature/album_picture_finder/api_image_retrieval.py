from flask import Blueprint, request, jsonify
import os
import time
import numpy as np
from .image_processing import load_and_preprocess_image, center_data
from .pca_computation import compute_pca, project
from .image_similarity import compute_euclidean_distances, get_top_k_results
from .mapper_loader import load_mapper, get_audio_for_image

image_api = Blueprint('image_api', __name__)

# Parameter
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../test/dataset/image_dataset')

MAPPER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../test/dataset/mapper/mapper.json')

TARGET_SIZE = (128, 128)
NUM_COMPONENTS = 50  

# Load dataset images
filenames = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
image_features = []
for fname in filenames:
    path = os.path.join(IMAGE_DIR, fname)
    vec = load_and_preprocess_image(path, target_size=TARGET_SIZE)
    image_features.append(vec)
image_features = np.array(image_features)
X_centered, mean_vec = center_data(image_features)

# Compute PCA
projection_matrix, _ = compute_pca(X_centered, NUM_COMPONENTS)
projected_data = project(image_features, mean_vec, projection_matrix)

# Load mapper
mapper_data = load_mapper(MAPPER_PATH)

@image_api.route('/query_image', methods=['POST'])
def query_image():
    start_time = time.time()

    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_file = request.files['image']
    query_name = image_file.filename if image_file.filename else "query_temp.png"
    query_path = os.path.join(os.path.dirname(__file__), query_name)
    image_file.save(query_path)

    try:
        # Query processing
        q_vec = load_and_preprocess_image(query_path, target_size=TARGET_SIZE)
        q_proj = project(np.array([q_vec]), mean_vec, projection_matrix)[0]
        distances = compute_euclidean_distances(q_proj, projected_data)
        top_results = get_top_k_results(distances, filenames, k=5)

        final_results = []
        for (img_name, sim) in top_results:
            audio_file = get_audio_for_image(mapper_data, img_name)
            result_entry = {
                "image": img_name,
                "similarity": round(sim, 2)
            }
            if audio_file:
                result_entry["audio_file"] = audio_file
            final_results.append(result_entry)

        exec_time = round((time.time() - start_time)*1000)  # in ms
        output = {
            "query_image": query_name,
            "results": final_results,
            "execution_time": f"{exec_time}ms"
        }
        return jsonify(output), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Inisialisasi dataset
IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../test/dataset/image_dataset')


filenames = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg'))]
image_features = []
for fname in filenames:
    path = os.path.join(IMAGE_DIR, fname)
    vec = load_and_preprocess_image(path, target_size=TARGET_SIZE)
    image_features.append(vec)
image_features = np.array(image_features)
X_centered, mean_vec = center_data(image_features)

# Compute PCA
projection_matrix, _ = compute_pca(X_centered, NUM_COMPONENTS)
projected_data = project(image_features, mean_vec, projection_matrix)
