from flask import Flask
from flask_script import Manager
import os

app = Flask(__name__)
manager = Manager(app)

app.config["SECRET_KEY"] = 'super-duper-secret-ultra-key-2000'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://developer:BqEDaSnPv9G0GtWD@localhost:8889/college'

# Mail configuration
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = '465'
app.config["MAIL_USE_TSL"] = 'True'
app.config["MAIL_USE_SSL"] = 'True'
app.config["MAIL_USERNAME"] = os.environ.get('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')


