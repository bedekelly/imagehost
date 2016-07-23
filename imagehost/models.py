from . import db


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(length=128))
    filetype = db.Column(db.String(length=32))
    url = db.Column(db.String(length=512))

    def __init__(self, filename, filetype, url):
        self.filename = filename
        self.filetype = filetype
        self.url = url

    def to_dict(self):
        return dict(filename=self.filename, filetype=self.filetype,
                    url=self.url)