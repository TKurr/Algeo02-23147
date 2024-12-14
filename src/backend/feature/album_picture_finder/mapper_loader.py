import json
from typing import Dict, List

def load_mapper(mapper_path: str) -> List[Dict[str, str]]:
    """
    Load JSON mapper data.
    """
    with open(mapper_path, 'r') as f:
        data = json.load(f)
    return data

def get_audio_for_image(mapper_data: List[Dict[str, str]], image_name: str) -> str:
    """
    Given an image_name, find the corresponding audio_file from mapper_data.
    Return empty string if not found.
    """
    for entry in mapper_data:
        if entry.get("pic_name") == image_name:
            return entry.get("audio_file", "")
    return ""
