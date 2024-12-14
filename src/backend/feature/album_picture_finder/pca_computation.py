import numpy as np
from typing import Tuple

def compute_pca(X: np.ndarray, num_components: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute PCA using SVD. Returns (projection_matrix, singular_values).
    projection_matrix shape: (num_components, D)
    Note: num_components is fixed for now. Could be adapted to cover certain variance.
    """
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    # select top num_components
    projection_matrix = Vt[:num_components]
    return projection_matrix, S

def project(X: np.ndarray, mean_vector: np.ndarray, projection_matrix: np.ndarray) -> np.ndarray:
    """
    Project data X onto the PCA subspace defined by projection_matrix.
    X shape: (N, D), mean_vector: (D,), projection_matrix: (num_components, D)
    """
    X_centered = X - mean_vector
    return X_centered @ projection_matrix.T
