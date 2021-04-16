from flask import render_template, url_for, request, redirect
from flask_migrate import Migrate, MigrateCommand
from forms import LoginForm, RegisterForm
from initialization import app, manager
from db_models import db, Users, Posts


@app.route('/')
def index():
    return render_template('index.html', posts=Posts.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usr = Users.query.filter(Users.username == username).all()
        if usr:
            if password == usr[0].password:
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
            user = Users(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return render_template('register.html', form=form)
    else:
        return render_template('register.html', form=form)


@app.route('/profile')
def profile():
    return render_template('user.html')

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()