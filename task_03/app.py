# pip install Flask-SQLAlchemy
# передавать вместе с паролем и именем
# app.config['SQLALCHEMY_DATABASE_URI'] =
# 'mysql+pymysql://username:password@hostname/database_name'
# ---------------------//-----------------------------------
# postgresql+psycopg2://username:password@hostname/database_name
# hostname - адрес сервера базы данных, а database_name - имя базы данных
from flask import Flask, redirect, render_template, request, flash, url_for
from flask_sqlalchemy import SQLAlchemy
# from models import User,Post,Comment
from task_03.models import db, User, Post, Comment

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


# db.init_app(app)
@app.route('/')
def hello_fun():
    if request.method == 'POST':
        flash('Форма успешно отправлена!', 'success')
        name = request.form.get('name')
        return redirect(url_for('hello_fun'))
    return render_template("index.html", h1="Главная страница")

@app.route('/event/', methods=['POST'])
def add_event():
    count = 5
    # Добавляем пользователей
    for user in range(1, count + 1):
        new_user = User(username=f'user{user}', email=f'user{user}@mail.ru')
        db.session.add(new_user)
        db.session.commit()
    # Добавляем статьи
    for post in range(1, count ** 2):
        author = User.query.filter_by(username=f'user{post % count + 1}').first()
        new_post = Post(title=f'Post title {post}', content=f'Post content {post}', author=author)
        db.session.add(new_post)
        db.session.commit()
    return 'ok'


@app.cli.command("init-db")
def init_db():
    db.create_all()
    # with app.app_context():
    #     db.create_all()
    print('OK')


@app.cli.command("add-john")
def add_user():
    user = User(username='john', email='john@example.com')
    db.session.add(user)
    db.session.commit()
    print('John add in DB!')


@app.cli.command("del-john")
def del_user():
    user = User.query.filter_by(username='john').first()
    db.session.delete(user)
    db.session.commit()
    print('Delete John from DB!')


@app.cli.command("fill-db")
def fill_tables():
    count = 5
    # Добавляем пользователей
    for user in range(1, count + 1):
        new_user = User(username=f'user{user}', email=f'user{user}@mail.ru')
        db.session.add(new_user)
        db.session.commit()
    # Добавляем статьи
    for post in range(1, count ** 2):
        author = User.query.filter_by(username=f'user{post % count + 1}').first()
        new_post = Post(title=f'Post title {post}', content=f'Post content {post}', author=author)
        db.session.add(new_post)
        db.session.commit()
@app.route('/users/')
def all_users():
    users = User.query.all()
    context = {'users': users}
    return render_template('users.html', **context)

if __name__ == "__main__":

    app.run(debug=True)