import os

import boto
from celery import Celery
from .models import File
from . import flask_app, db

app = Celery("imagehost.tasks", broker=flask_app.config["BROKER"])


def add_to_index(orig_filename, filetype, url):
    """Add a file to our index."""
    file = File(orig_filename, filetype, url)
    db.session.add(file)
    db.session.commit()


def s3_upload(dest_filename, orig_filename, filetype, filename):
    """Upload a file to S3."""
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


def generate_thumb(filename, filetype):
    known_types = {
        ""
    }


    if filetype in known_types:
        return known_types[filetype]

    with open(filename, "rb") as f:
        img_data = f.read()

    thumb_filename = filename + ".thumb.png"
    with open(thumb_filename) as f:
        f.write(thumb_data)
    return thumb_filename


@app.task(name="imagehost.tasks.process_file")
def process_file(filename, dest_filename, orig_filename, filetype):
    """Process a file by uploading it to S3 and adding it to our index."""
    url = s3_upload(dest_filename, orig_filename, filetype, filename)
    thumbnail_filename = generate_thumb(filename, filetype)
    thumbnail_url = s3_upload(thumbnail_filename, dest_filename+".thumb.png",
                              "", "")
    add_to_index(orig_filename, filetype, url, thumbnail_url)
    return dest_filename


def remove_from_index(s3_url):
    """Remove an entry in our files index by its S3 URL."""
    File.query.filter_by(url=s3_url).delete()
    db.session.commit()


def remove_from_s3(s3_url):
    """Remove a key from the S3 store by its URL."""
    raise NotImplementedError("Remove a key from the S3 store.")


@app.task(name="imagehost.tasks.delete_file")
def delete_file(s3_url):
    """Delete a file based on its S3 URL (which is unique)."""
    remove_from_index(s3_url)
    remove_from_s3(s3_url)