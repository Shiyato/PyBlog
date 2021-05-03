from flask import render_template, url_for, request, redirect
from flask_migrate import Migrate, MigrateCommand
from forms import LoginForm, RegisterForm
from initialization import app, manager, login_manager
from db_models import db, User, Post, update_table, make_role
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user
from func import time_format

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts, User=User, time_format=time_format)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usr = User.query.filter(User.username == username).first()
        if usr:
            if check_password_hash(usr.password, password):
                login_user(usr)
                return render_template('sucsses.html', username=username)
            else:
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)



@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        username = form.username.data
        email = form.email.data
        password = form.password.data

        try:
            user = User(username=username, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route('/profile')
@login_required
def profile():
    return render_template('user.html', username="none")

@manager.command
def uptable(table:str, id_column:str, id_column_value:str, conditions=None, **column_value):
    update_table(table, column_value, id_column, id_column_value, conditions)

@manager.command
def makerole(usernames, role, conditions=None):
    make_role(usernames, role, conditions)


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()