import cv2
import numpy as np

def load_and_preprocess_image(image_path: str, target_size=(128, 128)) -> np.ndarray:
    """
    Load image, convert to grayscale, resize to target_size, and flatten into 1D vector.
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, target_size)
    flattened = resized.flatten().astype(np.float32).tolist()
    return flattened

def center_data(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
    Center the data (mean subtraction).
    Returns (X_centered, mean_vector).
    data shape: (num_samples, num_features)
    """
    mean_vector = np.mean(data, axis=0)
    X_centered = data - mean_vector
    return X_centered, mean_vector
