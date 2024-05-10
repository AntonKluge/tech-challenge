import os

from flask import Flask, request, jsonify
import werkzeug
from werkzeug.utils import secure_filename

from lens_gpt_backend.gpt_call import get_producer_model
from lens_gpt_backend.lens_scape import get_urls_for_image

app = Flask(__name__)


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


def _process_image(file: werkzeug.datastructures.FileStorage) -> dict[str, str]:
    filename = secure_filename(file.filename)
    file_path = os.path.join("tmp", filename)
    absolute_path = os.path.abspath(file_path)
    try:
        file.save(absolute_path)
        urls = get_urls_for_image(absolute_path)
        classified = get_producer_model(urls)
        return classified
    except Exception as e:
        print(e)
        raise e
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
