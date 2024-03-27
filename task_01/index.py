
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/index/')
def main_page():
    return render_template('index.html', h1="Главная страница")

@app.route('/about_shoes/')
def get_page_shoes():
    return render_template("about_shoes.html", h1="Обувь")

@app.route('/about_outerwear/')
def get_page_outerwear():
    return render_template("about_outerwear.html", h1="Верхняя одежда")

@app.route('/about_trousers/')
def get_page_trousers():
    return render_template("about_trousers.html", h1="Штаны")

@app.route('/test/')
def get_page_test():
    return render_template("test.html", h1="text-test")
if __name__ == '__main__':
    app.run(debug=True)