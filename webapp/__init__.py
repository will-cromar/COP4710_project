from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")

from flask_bootstrap import Bootstrap

Bootstrap(app)

import mysql.connector

db = mysql.connector.connect(
    host=app.config["MYSQL_HOST"],
    user="root",
    password="mypassword",
    database=app.config["MYSQL_DB"],
    buffered=True,
)

from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

from webapp import views # flake8: noqa
