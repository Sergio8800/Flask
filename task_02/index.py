import logging
from pathlib import PurePath, Path
from venv import logger

from flask import Flask, url_for, render_template, request, redirect, flash, make_response
from markupsafe import escape
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key =b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    context = {
        'title': 'Главная',
        'name': 'Харитон'
    }
    response = make_response(render_template('main.html',
                                             **context))
    response.headers['new_head'] = 'New value'
    response.set_cookie('username', context['name'])
    # response = make_response("Cookie установлен")
    # response.set_cookie('username', 'admin')
    return response
@app.route('/getcookie/')
def get_cookies():
# получаем значение cookie
    name = request.cookies.get('username')
    return f"Значение cookie: {name}"

# Экранирование пользовательских данных escape()
# http://127.0.0.1:5000/<script>alert("I am haсker")</script>/

# @app.route('/<path:file>/')
# def get_file(file):
#     print(file)
#     return f'Ваш файл находится в: {escape(file)}!'

# Генерация url адресов

@app.route('/test_url_for/<int:num>/')
def test_url(num):
    text = f'<h3>В num лежит {num}</h3><br>'
    text += f'<h2>Функция {url_for("test_url", num=42) = }<br>'
    text += f'Функция {url_for("test_url", num=42,data="new_data") = }<br>'
    text += f'Функция {url_for("test_url", num=42,data="new_data", pi=3.14515) = }</h2><br>'

    return text
@app.route('/index2/')
def get_page_trousers():
    return render_template("base.html")

#  http://127.0.0.1:5000/get/?name=alex&age=13&level=80 для примера ввести в адрессную строку
# Похоже ты опытный игрок, раз имеешь уровень80
# ImmutableMultiDict([('name', 'alex'), ('age', '13'), ('level', '80')])
@app.route('/get/')
def get():
    if level := request.args.get('level'):
        text = f'Похоже ты опытный игрок, раз имеешь уровень{level}<br>'
    else:
        text = 'Привет, новичок.<br>'
    return text + f'{request.args}'

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        flash('Форма успешно отправлена!', 'success')
        name = request.form.get('name')
        return redirect(url_for('submit'))
        # return f'Hello {name}!'
    return render_template('form.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads',
        file_name))
        return f"Файл {file_name} загружен на сервер"
    return render_template('upload.html')

@app.errorhandler(404)
def page_not_found(e):
    logger.warning(e)
    context = {
    'title': 'Страница не найдена',
    'url': request.base_url,
    }
    return render_template('404.html', **context), 404

@app.route('/redirect/')
def redirect_to_index():
    return redirect(url_for('https://google.com'))



if __name__ == '__main__':
    app.run(debug=True)