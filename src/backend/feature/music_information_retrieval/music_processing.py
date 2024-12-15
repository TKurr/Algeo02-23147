import os
import numpy as np
from mido import MidiFile
from datetime import datetime
import librosa

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

def wav_processing(file_path, window_size=40, step_size=4, sr=22050):
    y, sr = librosa.load(file_path, sr=sr)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for i in range(pitches.shape[1]):  
        pitch_frame = pitches[:, i]
        magnitude_frame = magnitudes[:, i]
        if np.max(magnitude_frame) > 0: 
            pitch = pitch_frame[np.argmax(magnitude_frame)]
        else:
            pitch = 0  
        pitch_values.append(pitch)
    
    pitch_values = np.array(pitch_values)
    
    segments = []
    for i in range(0, len(pitch_values) - window_size + 1, step_size):
        segment = pitch_values[i:i + window_size]
        segments.append(segment)
    
    return segments

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

def process_all_wav(wav_files_paths, query_file_path, window_size=40, step_size=4):
    # Load query WAV file
    query_segments = wav_processing(query_file_path, window_size=window_size, step_size=step_size)
    query_feature_vectors = [
        generate_histogram(segment, bins=128, value_range=(0, 127))
        for segment in query_segments
    ]
    query_vector = np.mean(query_feature_vectors, axis=0)

    # Process dataset WAV files
    processed_data = []
    for file_path in wav_files_paths:
        try:
            segments = wav_processing(file_path, window_size=window_size, step_size=step_size)
            segment_features = [
                generate_histogram(segment, bins=128, value_range=(0, 127))
                for segment in segments
            ]
            feature_vector = np.mean(segment_features, axis=0)
            processed_data.append((os.path.basename(file_path), feature_vector))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Calculate similarities
    similarities = [
        (file_name, calculate_similarity(query_vector, feature_vector))
        for file_name, feature_vector in processed_data
    ]
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities

def process_all_audio(file_paths, query_file_path, file_type, window_size=40, step_size=4):
    if file_type not in ["midi", "wav"]:
        raise ValueError("Unsupported file type. Only 'midi' and 'wav' are allowed.")

    # Load query file
    if file_type == "midi":
        try:
            query_midi = MidiFile(query_file_path)
            query_segments = process_midi(query_midi, window_size, step_size)
        except Exception as e:
            raise ValueError(f"Error loading MIDI file: {e}")
    elif file_type == "wav":
        try:
            query_segments = wav_processing(query_file_path, window_size, step_size)
        except Exception as e:
            raise ValueError(f"Error loading WAV file: {e}")

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

    # Process dataset files
    processed_data = []
    for file_path in file_paths:
        try:
            if file_type == "midi":
                midi = MidiFile(file_path)
                segments = process_midi(midi, window_size, step_size)
            elif file_type == "wav":
                segments = wav_processing(file_path, window_size, step_size)

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
            processed_data.append((os.path.basename(file_path), feature_vector))
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Calculate similarities
    similarities = []
    for file_name, feature_vector in processed_data:
        similarity_score = calculate_similarity(query_vector, feature_vector)
        similarities.append((file_name, similarity_score))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities