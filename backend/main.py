import os
from flask import Flask
from flask_cors import CORS
from app.cache import cache
from app.celery import make_celery
from app import client

current_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='./mail/templates')
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

CORS(app, resources={r'/*': {'origins': '*'}})
cache.init_app(app)


app.app_context().push()
make_celery(client, app)

from app.controllers import *

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True,
        port=5000
    )
