# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app import routes
