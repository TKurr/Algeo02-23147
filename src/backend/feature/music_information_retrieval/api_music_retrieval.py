from flask import Blueprint, request, jsonify
import os
from .music_processing import process_all_midi, process_all_wav, process_all_audio

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
        dataset = []
        if query_file_path.endswith('.wav'):
            file_type = "wav"
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.wav'):
                        dataset.append(os.path.join(root, file))
        elif query_file_path.endswith('mid') or query_file_path.endswith('midi'):
            file_type = "midi"
            for root, _, files in os.walk(base_path):
                for file in files:
                    if file.endswith('.mid') or file.endswith('.midi'):
                        dataset.append(os.path.join(root, file))
 

        # if not midi_files_paths:
        #     return jsonify({"error": "No MIDI files found in the dataset."}), 400

        # Process the MIDI files using the algorithm logic from music_processing.py
        # if query_file_path.endswith('mid') or query_file_path.endswith('midi'): 
        #     similarities = process_all_midi(dataset, query_file_path)
        # elif query_file_path.endswith('.wav'):
        #     similarities = process_all_wav(dataset, query_file_path)
        similarities = process_all_audio(dataset, query_file_path, file_type, window_size=40, step_size=4)

        # Clean up temporary query file after comparison
        os.remove(query_file_path)

        # Return the results as JSON
        results = [{"file_name": file_name, "similarity_score": score} for file_name, score in similarities]
        return jsonify({"results": results}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
