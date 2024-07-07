import hashlib
import os
import uuid
from typing import Generator

from diskcache import Cache
from flask import Flask, request, jsonify, Response, g
from werkzeug.datastructures import FileStorage

from lens_gpt_backend.processing import process_async
from lens_gpt_backend.utils.product import Product
from lens_gpt_backend.utils.result_queue import ResultQueue

app = Flask(__name__, static_folder=os.path.abspath('../templates'))
cache = Cache(".cache")
if not os.path.exists("tmp"):
    os.makedirs("tmp")


@app.before_request
def before_request() -> None:
    request_id = str(uuid.uuid4())
    g.request_id = request_id


@app.route('/')
def index() -> Response:
    return app.send_static_file('index.html')


@app.route('/classify', methods=['POST'])
def upload_file() -> tuple[Response, int] | Response:
    request_id = g.request_id

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename and file.filename.endswith('.png'):
        generator = _process_image(file, request_id)
        return Response(generator, mimetype='text/event-stream')

    return jsonify({"error": "Unsupported file type"}), 400


def _process_image(file: FileStorage, request_id: str) -> Generator[str, None, None]:
    if not file or not file.filename:
        raise ValueError("No file provided.")

    file_hash = _hash_file_storage(file)
    file_path = os.path.join("tmp", file_hash + ".png")
    absolute_path = os.path.abspath(file_path)

    try:
        file.save(absolute_path)
        result_queue = ResultQueue.factory(file_hash)
        if result_queue.is_fresh():
            process_async(file_hash, lambda x: x.produce(Product(absolute_path)))
        return result_queue.str_generator(request_id)
    except Exception as e:
        print(e)
        raise e


def _hash_file(filepath: str) -> str:
    """Hashes the file using SHA-256 and returns the hash as a hexadecimal string."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def _hash_file_storage(file_storage: FileStorage, hash_algorithm: str = 'sha256') -> str:
    hash_obj = hashlib.new(hash_algorithm)
    chunk_size = 4096
    file_storage.stream.seek(0)  # Ensure stream is at the beginning
    while chunk := file_storage.stream.read(chunk_size):
        hash_obj.update(chunk)
    file_storage.stream.seek(0)  # Reset stream to the beginning after reading
    return hash_obj.hexdigest()
