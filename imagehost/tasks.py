import os

import boto
from celery import Celery
from .models import File
from . import flask_app, db

app = Celery("imagehost.tasks", broker=app.config["BROKER"])


def add_to_index(orig_filename, filetype, url):
    file = File(orig_filename, filetype, url)
    db.session.add(file)
    db.session.commit()


def s3_upload(dest_filename, orig_filename, filetype, filename):
    connection = boto.connect_s3(flask_app.config["S3_KEY"],
                                 flask_app.config["S3_SECRET"])
    bucket = connection.get_bucket(flask_app.config["S3_BUCKET"])
    access_control = "public-read"
    upload_dir = flask_app.config["S3_UPLOAD_DIR"]
    key = os.path.join(upload_dir, dest_filename)
    remote_file = bucket.new_key(key_name=key)
    url = remote_file.generate_url(expires_in=0, query_auth=False)
    remote_file.metadata.update({
        "original_filename": orig_filename,
        "filetype": filetype,
        "Content-Type": "application/octet-stream"
    })
    remote_file.set_contents_from_filename(filename)
    remote_file.set_acl(access_control)
    return url


@app.task(name="imagehost.tasks.process_file")
def process_file(filename, dest_filename, orig_filename, filetype):
    url = s3_upload(dest_filename, orig_filename, filetype, filename)
    add_to_index(orig_filename, filetype, url)
    return dest_filename
