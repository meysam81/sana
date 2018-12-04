from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os
basedir = os.path.abspath(os.path.dirname(__file__))
dbpath = 'sqlite:///' + os.path.join(basedir, 'sana.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbpath
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.secret_key = os.urandom(16)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

import views
import models
