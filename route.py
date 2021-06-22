from flask import render_template, url_for, request, redirect, abort
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy import text
from forms import LoginForm, RegisterForm, ProfileEdit, FileField, PostCreateForm, Search
from initialization import app, manager, login_manager
from db_models import db, User, Post, update_table, make_role, Post_Likes, Saves
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user, user_logged_out
from func import time_format, pic_change_name, justify_text
from datetime import datetime
from PIL import Image

import os


folder_path = os.path.abspath('.')
post_images_folder = os.path.join(folder_path, 'static', 'images', 'posts_photos')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.after_request
def add_header(r):
    """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
    """
    r.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r



@app.route('/')
def index():


    if current_user.is_authenticated:
        posts = Post.query.filter(Post.user_id != current_user.id).all()
    else:
        posts = Post.query.all()


    return render_template('index.html', posts=posts, User=User, time_format=time_format,
                           current_user=current_user, len=len, str=str, int=int, os=os, post_images_folder=post_images_folder,
                           post_likes=Post_Likes, post_saves=Saves, bool=bool, search=Search())

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect('/profile/' + current_user.username)
    else:
        form = RegisterForm()
        if form.validate_on_submit():
            print('Validate')
            username = form.username.data
            email = form.email.data
            password = form.password.data
            try:
                user = User(username=username, email=email, password=generate_password_hash(password))
                db.session.add(user)
                db.session.commit()
                folder_path = os.path.abspath('.')
                img = Image.open(folder_path + '//static//images//Pblog-user.jpg')
                img = img.convert('RGB')
                img = img.resize((200, 200))
                img.save(folder_path + '//static//images//users_photos//' + username + '.jpg')
                login_user(User.query.filter(User.username == username).first())
                query = text(f"UPDATE users SET is_online=True WHERE id='{current_user.id}'")
                db.engine.execute(query)
                return redirect('/')
            except:
                pass
    return render_template('register.html', form=form, current_user=current_user, search=Search())


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect('/profile')
    elif form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        usr = User.query.filter(User.username == username).first()
        if usr and check_password_hash(usr.password, password):
            login_user(usr, remember=form.remember.data)
            query = text(f"UPDATE users SET is_online=True WHERE id='{current_user.id}'")
            db.engine.execute(query)
            return redirect('/profile/' + username)
    return render_template('login.html', form=form, current_user=current_user, search=Search())



@app.route('/logout')
@login_required
def logout():
    query = text(f"UPDATE users SET last_online_date='{datetime.utcnow()}', is_online=False WHERE id='{current_user.id}'")
    db.engine.execute(query)
    logout_user()
    return redirect('/')


@app.route('/profile/<username>')
def profile(username):
    user = User.query.filter(User.username == username).first()
    if user:
        posts = Post.query.filter(Post.user_id == user.id).all()
        return render_template('user.html', time_format=time_format, current_user=current_user, user=user, posts=posts,
                               User=User, len=len, str=str, os=os, post_images_folder=post_images_folder, search=Search())
    else:
        abort(404)


@app.route('/profile-edit', methods=['POST', 'GET'])
@login_required
def profile_edit():
    #TODO сделать смену пароля
    form = ProfileEdit()
    if form.validate_on_submit():

        if form.photo.data:
            img = Image.open(form.photo.data)
            img = img.convert('RGB').resize((200,200))
            img.save(os.path.join(folder_path, 'static', 'images', 'users_photos', current_user.username + '.jpg'))

        if form.description.data:
            query = text(f"UPDATE users SET description='{form.description.data}' WHERE id='{current_user.id}'")

            db.engine.execute(query)

        username = form.username.data
        if username and username != current_user.username:
            query = text(f"UPDATE users SET username='{username}' WHERE id='{current_user.id}'")
            pic_change_name(current_user.username + '.jpg', username + '.jpg')
            db.engine.execute(query)

        return redirect('/profile/' + username if username else '/profile/' + current_user.username)
    return render_template('profile-edit.html', form=form, current_user=current_user, search=Search())


@app.route('/create-post', methods=['POST', 'GET'])
@login_required
def post_create():
    form = PostCreateForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=justify_text(form.post_content.data), user_id=current_user.id)
        db.session.add(post)
        db.session.commit()

        post = Post.query.order_by(Post.id.desc()).first()
        os.mkdir(os.path.join(post_images_folder, str(post.id)))

        if form.pre_view.data:
            img = Image.open(form.pre_view.data)
            img = img.convert('RGB').resize((500,500))
            img.save(os.path.join(post_images_folder, str(post.id), 'title_photo.jpg'))

            query = text(f"UPDATE posts SET have_title_image='1' WHERE id='{post.id}'")
            db.engine.execute(query)

        return redirect('/profile/' + current_user.username)
    return render_template('post-create.html', form=form, current_user=current_user, search=Search())

@app.route('/post/<id>')
def post_view(id):
    table = Post_Likes
    if current_user.is_authenticated:
        liked = bool(table.query.filter(table.post_id == id).filter(table.user_id == current_user.id).first())
        saved = bool(Saves.query.filter(Saves.post_id == id).filter(Saves.user_id == current_user.id).first())
    else:
        liked = False
        saved = False

    return render_template('post-page.html', current_user=current_user, post=Post.query.get(id), str=str, int=int,
                           liked=liked, saved=saved , table=table, search=Search())

@app.route('/like/post/<string:id>/<int:liked>')
@login_required
def like_post(id, liked):
    user_id = current_user.id
    if liked:
        query = text(f"DELETE FROM post_likes WHERE user_id='{user_id}' AND post_id='{id}';")
        db.engine.execute(query)
    else:
        like = Post_Likes(post_id=id, user_id=user_id)
        db.session.add(like)
        db.session.commit()
    return redirect(f'/post/{id}')


@app.route('/save/post/<string:id>/<int:liked>')
@login_required
def save_post(id, liked):
    user_id = current_user.id
    if liked:
        query = text(f"DELETE FROM saves WHERE user_id='{user_id}' AND post_id='{id}';")
        db.engine.execute(query)
    else:
        save = Saves(post_id=id, user_id=user_id)
        db.session.add(save)
        db.session.commit()
    return redirect(f'/post/{id}')


@app.route('/saved')
@login_required
def saved():
    saved_posts_id = list(map(lambda x: x.post_id,  Saves.query.filter(Saves.user_id == current_user.id).all()))
    saved_posts = list(filter(lambda x: x.id in saved_posts_id, Post.query.all()))
    return render_template('saved.html', current_user=current_user, posts=saved_posts, post_images_folder=post_images_folder,
                           post_likes=Post_Likes, time_format=time_format, User=User, search=Search(), len=len, str=str, int=int, bool=bool, os=os)


@app.route('/search', methods=['GET', 'POST'])
def search_view():
    form = Search()
    if form.validate_on_submit():
        to_find = form.search_field.data
        posts_found = list(filter(lambda post: to_find.lower() in post.title.lower(), Post.query.all()))
        users_found = list(filter(lambda user: to_find.lower() in user.username.lower(), User.query.all()))
        if (not posts_found and not users_found) or not to_find:
            message = 'По вашему запросу ничего не найдено'
        else:
            message = ''
    else:
        message = 'Вы пока ещё ничего не искали'
        posts_found = []
        users_found = []
    return render_template('search.html', current_user=current_user, search=form, posts_found=posts_found, users_found=users_found,
                           message=message, len=len, User=User, time_format=time_format,
                            str=str, int=int, os=os, post_images_folder=post_images_folder,
                           post_likes=Post_Likes, post_saves=Saves, bool=bool)

@manager.command
def uptable(table, column_value, id_column, id_column_value, conditions):
    if conditions == 'None':
        conditions = None
    update_table(table, column_value, id_column, id_column_value, conditions)

@manager.command
def makerole(username, role, conditions):
    if conditions == 'None':
        conditions = None
    make_role(username, role, conditions=conditions)


migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()