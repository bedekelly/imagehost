from flask import Flask
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__)
from . import config
db = SQLAlchemy(flask_app)
from . import models
from . import views