import hashlib
import os

from diskcache import Cache
from flask import Flask, request, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from lens_gpt_backend.producer.gpt_call import get_producer_model
from lens_gpt_backend.producer.lens_scape import get_urls_for_image

app = Flask(__name__)
cache = Cache(".cache")
if not os.path.exists("tmp"):
    os.makedirs("tmp")


generators = [
    ("producer_model", get_producer_model),
    ("producer_website", get_producer_website)
]


@app.route('/classify', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.png'):
        response = _process_image(file)
        return jsonify(response)
    else:
        return jsonify({"error": "Unsupported file type"}), 400


def _process_image(file: FileStorage) -> dict[str, str]:
    filename = secure_filename(file.filename)
    file_path = os.path.join("tmp", filename)
    absolute_path = os.path.abspath(file_path)

    try:
        file.save(absolute_path)
        file_hash = _hash_file(absolute_path)
        if file_hash in cache:
            print("Returning cached result.")
            return cache[file_hash]
        else:
            classified = _process_and_cache_image(file_hash, absolute_path)
            return classified
    except Exception as e:
        print(e)
        raise e
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def _hash_file(filepath: str) -> str:
    """Hashes the file using SHA-256 and returns the hash as a hexadecimal string."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def _process_and_cache_image(file_hash: str, file_path: str) -> dict[str, str]:
    """Process the image that has a given hash and path. Cache the result using the hash as the key."""
    try:
        urls = get_urls_for_image(file_path)
        classified = get_producer_model(urls)
        cache[file_hash] = classified
        return classified
    except Exception as e:
        print(f"Error processing image with hash {file_hash}: {e}")
        raise
