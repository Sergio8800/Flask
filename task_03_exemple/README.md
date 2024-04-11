# Инструменты и ссылки
## Ссылки на скачивание инструментов и примеров
- [Простой пример лабораторной](https://github.com/hvorovk/flask-lab-example)
- [Ссылка на скачивание Python](https://www.python.org/downloads/)

## Ссылки на документацию
- [Документация по языку Python3](https://docs.python.org/3/)
- [Документация по Flask](http://flask.pocoo.org/docs/0.12/)

## Учебники (дополнительная литература)
- [Викиучебник по Flask](https://ru.wikibooks.org/wiki/Flask)
- [Самоучитель по Python](https://pythonworld.ru/samouchitel-python)
- [Мега-учебник по Flask](https://habrahabr.ru/post/346306/)
- [Перевод официальной документации по Flask(версия 0.10.1)](http://flask-russian-docs.readthedocs.io/ru/latest/quickstart.html)
- [Памятка по virtualenv](https://eax.me/python-virtualenv/)
- [Документация по Jinja](http://jinja.pocoo.org/docs/2.10/)
- [Русская документация по Jinja](http://xgu.ru/wiki/Jinja2)
- [Небольшой самоучитель по Jinja](http://lectureswww.readthedocs.io/6.www.sync/2.codding/3.templates/jinja2.html)
- [Документация по Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.3/)
- [Установка virtualevwwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)

# Краткая теория

**Python** - высокоуровневый язык программирования общего назначения, ориентированный на повышение производительности разработчика и читаемости кода. Синтаксис ядра Python минималистичен. В то же время стандартная библиотека включает большой объём полезных функций.

**Python** поддерживает несколько парадигм программирования, в том числе структурное, объектно-ориентированное, функциональное, императивное и аспектно-ориентированное. Основные архитектурные черты — динамическая типизация, автоматическое управление памятью, полная интроспекция, механизм обработки исключений, поддержка многопоточных вычислений и удобные высокоуровневые структуры данных. Код в Python организовывается в функции и классы, которые могут объединяться в модули (они в свою очередь могут быть объединены в пакеты).

**Flask** - фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.

**Jinja2** - это шаблонизатор для языка программирования Python. Он подобен шаблонизатору Django, но предоставляет Python-подобные выражения, обеспечивая исполнение шаблонов в песочнице. Это текстовый шаблонизатор, поэтому он может быть использован для создания любого вида разметки, а также исходного кода.

**SQLAlchemy** - это программная библиотека на языке Python для работы с реляционными СУБД с применением технологии ORM. Служит для синхронизации объектов Python и записей реляционной базы данных. SQLAlchemy позволяет описывать структуры баз данных и способы взаимодействия с ними на языке Python без использования SQL.

### Hello World! на Flask


``` Python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
```

Для запуска нам всего лишь нужно выполнить данный скрипт интерпретатором Python с установленными зависимостями.

```bash
python3 hello.py
```

Первой строчкой мы импортируем основной модуль микрофреймворка Flask, следующей строчкой создаем экзепляр класса, далее с помощью декоратора **@app.route("%path%")** мы указываем, что по данному адресу мы должны вызывать нашу функцию. Далее функция которая возвращает строку "Hello World!". И наконец вызываем запуск сервера.

Данный фреймворк можно спокойно использовать для маленьких сайтов, блогов. Когда например не охото тянуть Django (Гораздо больший фреймворк). Или когда нужно выводить статистику по программе в веб. 

### Пример шаблона Jinja2

```html
<html>
    <head>
        <title>{{ title }}</title>
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```

Для того чтобы вместо {{ user.username }}, появилось имя, нам необходимо вызвать функцию render'a у шаблонизатора, а так же передать в render, словарь с именем **user**, с ключом username, и значением %UserName%. После этого мы получим готовую html страничку(или любого другого формата, который поддерживает шаблонизатор).

Пример для вызова render'а из Flask

```python
from flask import Flask
app = Flask(__name__)
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Goose'}
    return render_template('index.html', title='Home', user=user)

if __name__ == "__main__":
    app.run()
```

# Порядок выполнения

1. Скачать и установить Python3 последней версии.
    - Для Windows необходимо с сайта скачать нужный исполняемый файл и установить Python
    - для Linux нужно воспользоваться пакетным менеджером системы и установить Python
2. Создать папку для будущего проекта.
3. Настраиваем виртуальное окружение с помощью virtualenvwrapper. [инструкция](http://virtualenvwrapper.readthedocs.io/en/latest/install.html)
4. В виртуальном окружении необходимо установить зависимости. Из данного репозитория нужно скачать файл requirements.txt. Даллее выполняем команду:
```bash
pip3 install -r requirements.txt
```
5. Необходимо импортировать существующую базу. Для этого выполняем команду:
```bash
flask-sqlacodegen --flask --outfile models.py mysql+pymysql://user-name:password@host:port/db-schema
```

- models.py - название файла в котором будут размещены модели.
- user-name - имя юзера для входа в систему
- password  - пароль для этого пользователя
- host      - адрес хоста на котором поднят mysql
- port      - порт хоста на котором поднят mysql
- db-schema - нужная база данных

Пример модели:


```python
class Flat(db.Model):
    __tablename__ = 'Flat'
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer, nullable=False)
    owner_id = db.Column(db.ForeignKey('Owner.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    house_id = db.Column(db.ForeignKey('House.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    num = db.Column(db.Integer, nullable=False)

    house = db.relationship('House', primaryjoin='Flat.house_id == House.id', backref='flats')
    owner = db.relationship('Owner', primaryjoin='Flat.owner_id == Owner.id', backref='flats')
```

6. Созадим необходимую структуру:
    
```bash
    mkdir static/
    mkdir templates/
```

7. Создадим основной файл приложения. Назовем его **app.py**

В нем необходимо написать:

```python
from flask import render_template
from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'name'}
    return render_template('index.html', title='Home', user=user)

if __name__ == "__main__":
    app.run()
```

8. Создадим прстой шаблон в папку templates

```jinja
<html>
    <head>
        <title>{{ title }} - Microblog</title>
    </head>
    <body>
        <h1>Hello, {{ user.username }}!</h1>
    </body>
</html>
```

9. Запускаем наше приложение.
