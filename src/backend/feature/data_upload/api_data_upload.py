from flask import Blueprint, request, jsonify
from pathlib import Path
import shutil
import zipfile
import tarfile
import os
from pyunpack import Archive

# Define the Blueprint for file uploads
upload_api = Blueprint("upload_api", __name__)

# Define the base upload folder
BASE_UPLOAD_FOLDER = Path("test/dataset")
BASE_UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def extract_archive(file_path: Path, destination: Path):
    """
    Extract supported archives (.zip, .tar, .tar.gz, .rar, .7z) into the destination folder.
    """
    try:
        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as archive:
                archive.extractall(destination)
                print(f"Extracted ZIP: {file_path} -> {destination}")
        elif tarfile.is_tarfile(file_path):
            with tarfile.open(file_path, 'r:*') as archive:  # Handles .tar, .tar.gz, .tar.bz2
                archive.extractall(destination)
                print(f"Extracted TAR: {file_path} -> {destination}")
        else:
            # Use pyunpack for other formats like .rar and .7z
            try:
                Archive(str(file_path)).extractall(str(destination))
                print(f"Extracted {file_path.suffix.upper()}: {file_path} -> {destination}")
            except Exception as e:
                raise Exception(
                    f"Error extracting archive: {e}. Ensure `patool` and required tools (e.g., unrar, p7zip) are installed."
                )
    except Exception as e:
        raise Exception(f"Extraction failed: {str(e)}")


def save_file(file, destination: Path):
    """Save the uploaded file to the destination folder."""
    try:
        with destination.open("wb") as buffer:
            shutil.copyfileobj(file, buffer)
    except Exception as e:
        raise Exception(f"Failed to save file: {str(e)}")

@upload_api.route("/upload/<folder>", methods=["POST"])
def upload_files(folder):
    """
    Upload multiple files and handle archives (.zip, .tar, .rar, .7z, etc.).
    The files are saved to a folder based on the provided folder parameter.
    """
    if 'files' not in request.files:
        return jsonify({"error": "No files provided for upload."}), 400

    # Ensure the target folder exists
    target_folder = BASE_UPLOAD_FOLDER / folder
    target_folder.mkdir(parents=True, exist_ok=True)

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        file_path = target_folder / file.filename
        save_file(file, file_path)
        uploaded_files.append(file.filename)

        # Check if the file is an archive and extract it
        try:
            extract_archive(file_path, target_folder)
            file_path.unlink()  # Remove the archive after extraction
        except Exception as e:
            print(f"Skipping extraction for {file.filename}: {str(e)}")

    return jsonify({"message": f"Files uploaded successfully to {folder}", "files": uploaded_files})