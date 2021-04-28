from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from initialization import app

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(240), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Posts', backref='users', lazy=True)

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.password})"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    postdate = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Post({self.title}, {self.postdate}, {self.user_id})"