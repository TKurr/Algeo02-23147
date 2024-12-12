import numpy as np
from typing import List, Tuple

def compute_euclidean_distances(query_vec: np.ndarray, dataset_vecs: np.ndarray) -> np.ndarray:
    """
    Compute Euclidean distances between query_vec and each vector in dataset_vecs.
    query_vec shape: (num_components,)
    dataset_vecs shape: (N, num_components)
    """
    distances = np.linalg.norm(dataset_vecs - query_vec, axis=1)
    return distances

def get_top_k_results(distances: np.ndarray, filenames: List[str], k: int = 5) -> List[Tuple[str, float]]:
    """
    Sort results by ascending distance and return top_k.
    Using the specified formula:
    similarity_percentage = (1 - dist/max_dist)*100%
    """
    sorted_indices = np.argsort(distances)
    results = []
    max_dist = np.max(distances) if np.max(distances) != 0 else 1.0
    for idx in sorted_indices[:k]:
        sim_percent = 100.0 * (1.0 - distances[idx]/max_dist)
        results.append((filenames[idx], sim_percent))
    return results
