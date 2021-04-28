from flask import Flask
from flask_script import Manager
import os

app = Flask(__name__)
manager = Manager(app)

app.config["SECRET_KEY"] = 'super-duper-secret-ultra-key-2000'
app.config["SQLALCHEMY_DATABASE_URI"] = None

# Mail configuration
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_USE_TSL"] = 'True'
app.config["MAIL_USE_SSL"] = 'True'
app.config["MAIL_PORT"] = '465'
app.config["MAIL_USERNAME"] = 'zhdanov.ph@gmail.com'
app.config["MAIL_PASSWORD"] = 'iPRZtatiY33%'
app.config["MAIL_SENDER"] = app.config["MAIL_USERNAME"]
app.config["MAIL_LETTER_PREFIX"] = 'Py-blog - '

