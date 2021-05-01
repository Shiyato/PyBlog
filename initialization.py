from flask import Flask
from flask_script import Manager
from flask_login import LoginManager
import os

app = Flask(__name__)
manager = Manager(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.init_app(app)
#login_manager.login_view = 'login'


app.config["SECRET_KEY"] = 'super-duper-secret-ultra-key-2000'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://developer:password@localhost:8889/college'

# Mail configuration
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_USE_TSL"] = 'True'
app.config["MAIL_USE_SSL"] = 'True'
app.config["MAIL_PORT"] = '465'
app.config["MAIL_USERNAME"] = 'zhdanov.ph@gmail.com'
app.config["MAIL_PASSWORD"] = 'iPRZtatiY33%'
app.config["MAIL_SENDER"] = app.config["MAIL_USERNAME"]
app.config["MAIL_LETTER_PREFIX"] = 'Py-blog - '

