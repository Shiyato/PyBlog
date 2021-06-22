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
    description = db.Column(db.Text(), default=None)
    role = db.Column(db.String(30), nullable=False, default="user")
    register_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    is_online = db.Column(db.Boolean(), nullable=False, default=False)
    last_online_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    posts = db.relationship('Post', backref='users', lazy='dynamic')
    def __repr__(self):
        return f"User({self.username}, {self.email}, {self.password})"

class Coments(db.Model):
    __tablename__ = 'coments'
    id = db.Column(db.Integer, primary_key=True)
    sub_obj = db.Column(db.String(16), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    coment_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"))

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    postdate = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete="CASCADE"))
    have_title_image = db.Column(db.Boolean(), nullable=False, default=0)

    def __repr__(self):
        return f"Post({self.title}, {self.postdate}, {self.user_id}, {self.id})"

class Post_Likes(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=None)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"), nullable=None)

class Saves(db.Model):
    __tablename__ = 'saves'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=None)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete="CASCADE"), nullable=None)

def update_table(table:str, column_value:str, id_column:str, id_column_value:str, conditions=None):
    if conditions:
        query = text(f"UPDATE {table} SET {column_value}" if conditions == 'everyone' else f"UPDATE TABLE {table} SET {column_value} WHERE {conditions}")
    else:
        query = text(f"UPDATE {table} SET {column_value} WHERE {id_column} = '{id_column_value}'")
    db.engine.execute(query)

def make_role(username, role, conditions=None):
    update_table('users', f"role='{role}'", 'username', username, conditions=conditions)