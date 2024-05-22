import hashlib
import os
from typing import Generator

from diskcache import Cache
from flask import Flask, request, jsonify, Response
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from lens_gpt_backend.utils.result_queue import ResultQueue

app = Flask(__name__)
cache = Cache(".cache")
if not os.path.exists("tmp"):
    os.makedirs("tmp")


@app.route('/classify', methods=['POST'])
def upload_file() -> tuple[Response, int] | Response:
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename and file.filename.endswith('.png'):
        response = _process_image(file)
        return jsonify(response)

    return jsonify({"error": "Unsupported file type"}), 400


def _process_image(file: FileStorage) -> dict[str, str]:
    if not file or not file.filename:
        raise ValueError("No file provided.")

    filename = secure_filename(file.filename)
    file_path = os.path.join("tmp", filename)
    absolute_path = os.path.abspath(file_path)

    try:
        file.save(absolute_path)
        file_hash = _hash_file(absolute_path)



    except Exception as e:
        print(e)
        raise e
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def generate_upstream(file_hash: str, request_id: str) -> Generator[tuple[Response, int], None, None]:
    result_queue = ResultQueue(file_hash)
    yield result_queue.get_next(request_id)


def _hash_file(filepath: str) -> str:
    """Hashes the file using SHA-256 and returns the hash as a hexadecimal string."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()
