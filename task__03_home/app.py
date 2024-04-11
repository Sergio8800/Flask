import base64
import csv
import io
import random
from base64 import b64encode as enc64
from base64 import b64decode as dec64
from io import BytesIO

import pandas as pandas
from PIL import Image

from flask import Flask, render_template, session, request, flash, make_response, redirect, url_for, jsonify
import os
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from werkzeug.utils import secure_filename

from models import db, User, Post, LoginForm, RegistrationForm

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
# db = SQLAlchemy(app)
db.init_app(app)
app.app_context().push()
db.create_all()
print('DB is OK')


# name_from_cookie = "None"

def get_cookie():
    # global name_from_cookie
    name_from_cookie = request.cookies.get('name')
    return name_from_cookie


@app.route('/')
@app.route('/index/')
def index():
    # name = request.cookies.get('name')
    # parol = request.cookies.get('parol')
    # context = [name, parol]
    if 'username' in session:
        name = session['username']
    else:
        name = None
    context1 = get_cookie()
    return render_template('index.html', name=context1)


@app.route('/catalog/')
def catalog():
    if 'username' in session:
        name = session['username']
    else:
        name = None
    directory = "./static/img/"
    files = []
    context = list()
    files += os.listdir(directory)
    text = ["Kingston 555kv",
            "Kingsong KS-16X",
            "Гироскоп черный - 777 Втч",
            "Электрический одноколесный велосипед INMOTION V10F",
            "Airwheel Q3 Self-Balancing Electric Monoruota Men, черный, 51,8 x 40,8 x 20 см"]
    # context = dict(zip(files, text))
    for el, txt in zip(files, text):
        element = {"file": el, "text": txt}
        context.append(element)
    # print(context)
    return render_template('catalog.html', context=context, name=name)


@app.route('/autoris_form/', methods=['GET', 'POST'])
def autoris():
    # form = LoginForm()  ...and form.validate()
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('autoris'))
        else:
            new_user = User(username=request.form['name'], email='example@mail.com')
            User.query.delete()  # <<<<<<<< без этого удаления не работает
            db.session.add(new_user)
            db.session.commit()

            flash('Форма успешно отправлена! Вы залогинились, ваше имя сохранено', 'success')
        # Обработка данных формы

        name = request.form.get('name')
        password = request.form.get('Password')
        gender = request.form.get('Gender')

        response = make_response(render_template('autoris_form.html', name=name))
        response.set_cookie("name", request.form['name'])
        # response.headers['new_head'] = 'New value'
        session['username'] = request.form.get('name') or 'NoName'
        # name = request.form.get('name')
        # return render_template('autoris_form.html', contex=response)

        # return redirect(url_for('autoris'))
        return response
    return render_template('autoris_form.html', name=get_cookie())

@app.route('/logout/')
def logout():
    session.pop('username', None)
    if 'email' in session:
        session.pop('email', None)
    response = make_response("delete")
    response.set_cookie('name', '', max_age=0)
    response.delete_cookie('name')
    print(session.get('username'))
    return redirect(url_for('autoris'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        email = form.email.data
        password = form.password.data
        print(email, password)
    return render_template('register.html', form=form)


# ловим и обрабатываем ошибку, если файл больше 16мб
@app.errorhandler(413)
def too_large(e):
    return make_response(jsonify(message="File is too large"), 413)


@app.route('/users/')
def all_users():
    users = User.query.all()
    print(users)
    context = {'users': users}
    return render_template('users.html', **context)


# ==================== для проверки файла, что это фотография============
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/cat_auto/', methods=['GET', 'POST'])
def goods_create():
    if request.method == 'POST':
        title = request.form['name_goods']
        content = request.form['discription']
        photo = request.files['photo']
        if 'photo' in request.files and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            k = str(random.randint(1000, 99000))
            img_way = filename.split('.')[0] + k + "." + filename.split('.')[1]
            # Сохраняем файл локально
            local_folder = os.path.join('static/img', img_way)
            photo.save(local_folder)

            # Читаем файл как двоичный объект
            with open(local_folder, 'rb') as image_file:
                binary_data = image_file.read()
                # Сохраняем изображение в базе данных
                new_image = Post(title=title, content=content, img=binary_data, img_way=img_way)
                db.session.add(new_image)
                db.session.commit()

            return redirect(url_for('goods_create'))
            # return filename
        else:
            return 'No file part in the request', 400
        # flash('Форма успешно отправлена! Вы создали новый товар', 'success')
        # if not request.form['name']:
        #     flash('Введите имя!', 'danger')
        #     return redirect(url_for('autoris'))
        # else:
        #     new_user = User(username=request.form['name'], email='example@mail.com')
        #     User.query.delete() # <<<<<<<< без этого удаления не работает
        #     db.session.add(new_user)
        #     db.session.commit()
        #     flash('Форма успешно отправлена! Вы залогинились, ваше имя сохранено', 'success')
        # return redirect(url_for('goods_create'))
    context = all_goods()
    data_list = dict()
    for i in range(len(context['posts'])):
        image = base64.b64decode(context['posts'][i].img)

        pre_img = io.BytesIO(context['posts'][i].img)
        image = Image.open(pre_img)
        id = context['posts'][i].id
        title = context['posts'][i].title
        content = context['posts'][i].content
        img_way = context['posts'][i].img_way

        data_list.update({"id": id, "title": title, "content": content, 'image': image, 'img_way': img_way})
        print(data_list)
        # print(context['posts'])
        # context = {'posts': data_list}
    return render_template('catalog_automatiq.html', name=get_cookie(), **context, data_list=data_list)


def all_goods():
    posts = Post.query.all()
    context = {'posts': posts}
    return context


@app.route('/goods_up/<int:id>/', methods=['GET', 'POST'])
def goods_update(id):
    post = Post.query.get_or_404(id)
    print(post)
    if request.method == 'POST':
        post.title = request.form['name_goods']
        post.content = request.form['discription']
        photo = request.files['photo']
        if 'photo' in request.files and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            k = str(random.randint(1000, 99000))
            img_way = filename.split('.')[0] + k + "." + filename.split('.')[1]
            post.img_way = img_way
            # Сохраняем файл локально
            local_folder = os.path.join('static/img', img_way)
            photo.save(local_folder)

            # Читаем файл как двоичный объект
            with open(local_folder, 'rb') as image_file:
                binary_data = image_file.read()
                post.img = binary_data

        db.session.commit()
        return redirect(url_for('goods_create'))
    else:
        return render_template('update_goods.html', post=post)





@app.errorhandler(404)
def page_not_found(e):
    # logger.warning(e)
    context = {
        'title': 'Страница не найдена',
        'url': request.base_url,
    }
    return render_template('404.html', **context), 404


if __name__ == "__main__":
    # print(f'====={1%5}')
    app.run(debug=True)
