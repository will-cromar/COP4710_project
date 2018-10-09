from flask import Flask

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py")

import mysql.connector

db = mysql.connector.connect(
    host=app.config["MYSQL_HOST"],
    user="root",
    password="mypassword",
    database="Proj",
    buffered=True,
)

from webapp import views # flake8: noqa
