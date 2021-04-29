from flask import render_template, url_for, request, redirect
from flask_migrate import Migrate, MigrateCommand
from forms import LoginForm, RegisterForm
from initialization import app, manager, login_manager
from db_models import db, User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required


@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts, User=User)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usr = User.query.filter(User.username == username).all()
        if usr:
            if check_password_hash(usr[0].password, password):
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

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()