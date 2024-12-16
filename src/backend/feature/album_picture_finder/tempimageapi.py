from flask import Blueprint, request, jsonify
import os
from .tempimage import process_image, process_database, filter_similar_images

image_api = Blueprint('image_api', __name__)

@image_api.route('/query_image', methods=['POST'])
def find_similar_images():
    try:
        # Get the uploaded query file from the request
        query_file = request.files.get('query_file')

        if not query_file:
            return jsonify({"error": "Please provide a query image to compare."}), 400

        # Validate the file extension
        _, file_extension = os.path.splitext(query_file.filename)
        if file_extension.lower() not in ['.jpg', '.jpeg', '.png']:
            return jsonify({"error": "Invalid file type. Only .jpg, .jpeg, and .png are supported."}), 400

        # Save the query file temporarily
        temp_dir = os.path.join(os.getcwd(), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        query_path = os.path.join(temp_dir, 'temp_query_image' + file_extension)
        query_file.save(query_path)

        # Process the database (standardization and PCA computation)
        db_result = process_database()
        if db_result is None:
            os.remove(query_path)
            return jsonify({"error": "No images found in the database or an error occurred."}), 400

        standardized_vectors, filenames, pixel_average, Ut_reduced, num_components, new_size = db_result

        # Process the query image to find similar images
        distances = process_image(query_path)
        if distances is None:
            os.remove(query_path)
            return jsonify({"error": "Error processing the query image."}), 400

        # Define a similarity threshold
        similarity_threshold = 9792

        # Filter filenames of similar images based on the threshold
        similar_images = filter_similar_images(
            [distance[1] for distance in distances], filenames, threshold=similarity_threshold
        )

        # Clean up temporary query file
        os.remove(query_path)

        # Return the filenames of similar images
        return jsonify({"results": similar_images}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
