from flask import Blueprint, request, jsonify
import os
from .music_processing import process_all_midi

music_api = Blueprint('music_api', __name__)

@music_api.route('/compare_midi', methods=['POST'])
def compare_midi():
    try:
        # Get the uploaded query file from the request
        query_file = request.files.get('query_file')

        if not query_file:
            return jsonify({"error": "Please provide a query file to compare."}), 400

        # Define the fixed path for the dataset
        base_path = os.path.join(os.getcwd(), 'test/dataset/midi_dataset')
        query_path = os.path.join(os.getcwd(), 'test/query')

        # Save the query file to a temporary location
        query_file_path = os.path.join(query_path, 'temp_query.mid')
        query_file.save(query_file_path)

        # Get the list of MIDI files in the fixed dataset directory
        midi_files_paths = []
        for root, _, files in os.walk(base_path):
            for file in files:
                if file.endswith('.mid') or file.endswith('.midi'):
                    midi_files_paths.append(os.path.join(root, file))

        if not midi_files_paths:
            return jsonify({"error": "No MIDI files found in the dataset."}), 400

        # Process the MIDI files using the algorithm logic from music_processing.py
        similarities = process_all_midi(midi_files_paths, query_file_path)

        # Clean up temporary query file after comparison
        os.remove(query_file_path)

        # Return the results as JSON
        results = [{"file_name": file_name, "similarity_score": score} for file_name, score in similarities]
        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
