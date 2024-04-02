from flask import Flask, render_template, session, request, flash, make_response, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


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


    context = get_cookie()
    return render_template('index.html', name=context)


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
    if request.method == 'POST':
        if not request.form['name']:
            flash('Введите имя!', 'danger')
            return redirect(url_for('autoris'))
        else:
            flash('Форма успешно отправлена! Вы залогинились, ваше имя сохранено', 'success')
        # Обработка данных формы

        name = request.form.get('name')
        parol = request.form.get('parol')

        response = make_response(render_template('autoris_form.html', name=name))
        response.set_cookie("name", request.form['name'])
        # response.headers['new_head'] = 'New value'
        session['username'] = request.form.get('name') or 'NoName'
        # name = request.form.get('name')
        # return render_template('autoris_form.html', contex=response)

        # return redirect(url_for('autoris'))
        return response
    return render_template('autoris_form.html', name=get_cookie())


# @app.route('/index_autoris/')
# def index_autoris():
#     return render_template('index_autoris.html')


@app.route('/logout/')
def logout():
    session.pop('username', None)
    response = make_response("delete")
    # response.set_cookie('name', '', expires=0)
    response.delete_cookie('name')
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    # logger.warning(e)
    context = {
        'title': 'Страница не найдена',
        'url': request.base_url,
    }
    return render_template('404.html', **context), 404


if __name__ == "__main__":
    app.run(debug=True)
