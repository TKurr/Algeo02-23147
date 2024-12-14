import os
import numpy as np
from mido import MidiFile
from datetime import datetime

def process_midi(midi, window_size=40, step_size=4):
    notes = []
    for track in midi.tracks:
        for msg in track:
            if msg.type == 'note_on' and msg.velocity > 0:
                notes.append(msg.note)

    segments = segment_notes(notes, window_size, step_size)
    return segments


def segment_notes(notes, window_size, step_size):
    segments = []
    for i in range(0, len(notes) - window_size + 1, step_size):
        segment = notes[i:i + window_size]
        segments.append(segment)
    return segments


def normalize_tempo(notes):
    mean = np.mean(notes)
    std = np.std(notes) if np.std(notes) != 0 else 1
    normalized_notes = [(note - mean) / std for note in notes]
    return normalized_notes


def generate_histogram(data, bins, value_range):
    histogram, _ = np.histogram(data, bins=bins, range=value_range)
    normalized_histogram = histogram / \
        sum(histogram) if sum(histogram) != 0 else histogram
    return normalized_histogram


def calculate_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    cosine_similarity = dot_product / (norm_a * norm_b)
    return cosine_similarity

def process_all_midi(midi_files_paths, query_file_path, window_size=40, step_size=4):
    midi_files = []
    for file_path in midi_files_paths:  # Iterate directly over paths
        try:
            midi = MidiFile(file_path)
            file_name = os.path.basename(file_path)
            midi_files.append((file_name, midi))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Load the query file
    query_midi = MidiFile(query_file_path)
    query_segments = process_midi(query_midi, window_size=window_size, step_size=step_size)
    query_feature_vectors = []

    for segment in query_segments:
        normalized_notes = normalize_tempo(segment)
        atb_histogram = generate_histogram(normalized_notes, bins=128, value_range=(0, 127))
        rtb_histogram = generate_histogram(np.diff(normalized_notes), bins=255, value_range=(-127, 127))
        ftb_histogram = generate_histogram(
            [note - normalized_notes[0] for note in normalized_notes], bins=255, value_range=(-127, 127)
        )
        query_feature_vector = np.concatenate([atb_histogram, rtb_histogram, ftb_histogram])
        query_feature_vectors.append(query_feature_vector)

    query_vector = np.mean(query_feature_vectors, axis=0)

    processed_data = []
    for file_name, midi in midi_files:
        segments = process_midi(midi, window_size=window_size, step_size=step_size)
        segment_features = []

        for segment in segments:
            normalized_notes = normalize_tempo(segment)
            atb_histogram = generate_histogram(normalized_notes, bins=128, value_range=(0, 127))
            rtb_histogram = generate_histogram(np.diff(normalized_notes), bins=255, value_range=(-127, 127))
            ftb_histogram = generate_histogram(
                [note - normalized_notes[0] for note in normalized_notes], bins=255, value_range=(-127, 127)
            )
            feature_vector = np.concatenate([atb_histogram, rtb_histogram, ftb_histogram])
            segment_features.append(feature_vector)

        feature_vector = np.mean(segment_features, axis=0)
        processed_data.append((file_name, feature_vector))

    similarities = []
    for file_name, feature_vector in processed_data:
        similarity_score = calculate_similarity(query_vector, feature_vector)
        similarities.append((file_name, similarity_score))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities


def main():
    folder_path = os.path.join( os.getcwd(), "src/backend/test/dataset/midi_dataset").replace("\\", "/") # path dataset
    midi_files = []

    query_file_path = os.path.join(os.getcwd(), "src/backend/test/test_audio4.mid").replace("\\", "/") # path audio yang dibandingin (query)

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".midi") or file_name.endswith(".mid"):
            file_path = os.path.join(folder_path, file_name)
            midi = MidiFile(file_path)
            midi_files.append((file_name, midi))

    query_midi = MidiFile(query_file_path)
    query_segments = process_midi(query_midi, window_size=40, step_size=4)
    query_feature_vectors = []

    for segment in query_segments:
        normalized_notes = normalize_tempo(segment)
        atb_histogram = generate_histogram(
            normalized_notes, bins=128, value_range=(0, 127))
        rtb_histogram = generate_histogram(
            np.diff(normalized_notes), bins=255, value_range=(-127, 127))
        ftb_histogram = generate_histogram(
            [note - normalized_notes[0] for note in normalized_notes], bins=255, value_range=(-127, 127))
        query_feature_vector = np.concatenate(
            [atb_histogram, rtb_histogram, ftb_histogram])
        query_feature_vectors.append(query_feature_vector)

    query_vector = np.mean(query_feature_vectors, axis=0)

    processed_data = []
    for file_name, midi in midi_files:
        segments = process_midi(midi, window_size=40, step_size=4)
        segment_features = []

        for segment in segments:
            normalized_notes = normalize_tempo(segment)
            atb_histogram = generate_histogram(
                normalized_notes, bins=128, value_range=(0, 127))
            rtb_histogram = generate_histogram(
                np.diff(normalized_notes), bins=255, value_range=(-127, 127))
            ftb_histogram = generate_histogram(
                [note - normalized_notes[0] for note in normalized_notes], bins=255, value_range=(-127, 127))
            feature_vector = np.concatenate(
                [atb_histogram, rtb_histogram, ftb_histogram])
            segment_features.append(feature_vector)

        feature_vector = np.mean(segment_features, axis=0)
        processed_data.append((file_name, feature_vector))

    similarities = []
    for file_name, feature_vector in processed_data:
        similarity_score = calculate_similarity(query_vector, feature_vector)
        similarities.append((file_name, similarity_score))

    similarities.sort(key=lambda x: x[1], reverse=True)
    print("Hasil kemiripan dengan file query:")
    for file_name, score in similarities:
        print(f"{file_name}: {score:.4f}")


if __name__ == "__main__":
    main()
