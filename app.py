import logging
from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
import os
import logging
from rembg import remove
import time

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}


def environment():
    return os.environ['APP_ENV']


def production():
    return environment() == "production"


def development():
    return not production()


def log_filename():
    return "production.log" if production() else "development.log"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_name_without_ext(filename):
    return os.path.splitext(filename)[0]


def transform_file(input, output, filename):
    input += filename
    output += file_name_without_ext(filename) + ".png"
    with open(input, "rb") as i:
        with open(output, "wb") as o:
            input = i.read()
            output = remove(input)
            o.write(output)


if production():
    logging.basicConfig(filename=log_filename(), level=logging.DEBUG)


app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == os.environ['USERNAME'] and os.environ['PASSWORD'] == password:
        return True
    return False


@app.route("/remove_background", methods=["POST"])
@auth.login_required
def transform():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file in the request'}), 400

    file = request.files['image']

    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid image file type'}), 400

    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    if not os.path.exists('uploads/edited_file'):
        os.makedirs('uploads/edited_file')
    if not os.path.exists('uploads/original_file'):
        os.makedirs('original_file')

    timestamp = str(int(time.time() * 1000)) + "-"
    file_name = timestamp + file.filename

    file.save(os.path.join('uploads/original_file', file_name))

    transform_file('uploads/original_file/', 'uploads/edited_file/', file_name)

    return send_file('uploads/edited_file/' + file_name_without_ext(file_name) + ".png", mimetype='image/png')


@app.route("/get_image", methods=["GET"])
@auth.login_required
def get_image():
    filename = request.args.get('filename')
    original = request.args.get('original') or False
    if not filename:
        return {'error': 'Filename parameter is required.'}, 400

    if not allowed_file(filename):
        return jsonify({'error': 'Invalid image file type'}), 400
    if original:
        file_path = os.path.join('uploads/original_file', filename)
    else:
        file_path = os.path.join('uploads/edited_file', filename)

    try:
        return send_file(file_path, mimetype='image/png')
    except FileNotFoundError:
        return jsonify({'error': 'File not found.'}), 404


if __name__ == "__main__":
    app.run(debug=development(), port=8000, host="0.0.0.0")
