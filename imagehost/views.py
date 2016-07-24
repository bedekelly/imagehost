import os
from uuid import uuid4
from flask import render_template, request, jsonify

from . import flask_app
from .models import File, db
from .tasks import process_file


@flask_app.route("/upload")
def index():
    return render_template("upload.html")


@flask_app.route("/api/upload", methods=["POST"])
def upload():
    file = request.files["files[]"]
    src_filename = file.filename
    src_filename, src_ext = os.path.splitext(src_filename)
    dest_filename = uuid4().hex + src_ext
    temp_filepath = os.path.join("files", dest_filename)
    with open(temp_filepath, "wb") as local_file:
        local_file.write(file.stream.read())
    process_file.delay(temp_filepath, dest_filename, src_filename, src_ext)

    return jsonify(success="File uploaded"), 200


@flask_app.route("/api/files", methods=["GET"])
def get_files():
    return jsonify(files=[file.to_dict() for file in File.query.all()])


@flask_app.route("/api/files", methods=["DELETE"])
def delete_file():
    """
    Start a celery task to remove this file from our database and from the
    S3 bucket.
    """
    from .tasks import delete_file
    delete_file.delay(request.json)
    return jsonify(error="Not yet implemented!"), 501


@flask_app.route("/")
def view_files():
    return render_template("files.html")