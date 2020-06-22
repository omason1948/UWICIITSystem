from flask import Flask

from flask_login import LoginManager

app = Flask(__name__)
login = LoginManager()

from app import routes, errors
