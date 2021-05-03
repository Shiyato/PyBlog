from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from initialization import app
from flask_login import UserMixin

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="user")
    posts = db.relationship('Post', backref='users', lazy='joined')

    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.password})"


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    postdate = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"))

    def __repr__(self):
        return f"Post({self.title}, {self.postdate}, {self.user_id})"


def update_table(table:str, column_value:dict, id_column:str, id_column_value:str, conditions=None):
    column_value = ', '.join([f"{key} = {value}" for key, value in column_value.items()])
    if conditions:
        query = text(f"update table {table} set {column_value}" if conditions == 'everyone' else f"update table {table} set {column_value} where {conditions}")
    else:
        query = text(f"update table {table} set {column_value} where {id_column} = {id_column_value}")
    db.engine.execute(query)

def make_role(usernames, role, conditions=None):
    for user in usernames:
        update_table('users', {'role': f'{role}'}, 'username', user, conditions)