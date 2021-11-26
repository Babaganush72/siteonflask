from flask import Flask, render_template, url_for, request, redirect  # url_f - для работы со статик файлами и css
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # настраиваем базу данных с указанием на версию
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # он вскоре будет отключен, поэтому его надо выкл!
db = SQLAlchemy(app)


# работа с БД
class Article(db.Model):  # создаем таблицу
    id = db.Column(db.Integer, primary_key=True)  # поле с уникальным кодом айди
    title = db.Column(db.String(100), nullable=False)  # поле с текстом которое нельзя не заполнять null
    intro = db.Column(db.String(300), nullable=False)  # поле с текстом которое нельзя не заполнять null
    text = db.Column(db.Text, nullable=False)  # поле с текстом которое нельзя не заполнять null
    date = db.Column(db.DateTime, default=datetime.utcnow)  # устанавливаем время публикации

    def __repr__(self):
        return '<Article %r>' % self.id  # когда выбираем объект на основе этого класса будет выдовать его id


''' как импортировать базу данных:
- открываем в терминале питон командой python
- from ap import db
- db.create_all()
- exit()
'''


@app.route("/")  # декоратор который отслеживает главную страницу (имя страницы "/")
@app.route("/home")  # (имя страницы - рауты "/home")
def index():
    return render_template("index.html")  # подключает шаблоны html из папки темплатес


@app.route("/posts")
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()  # обращаемся к таблице бд и сортируем по дате
    return render_template("posts.html", articles=articles)


@app.route("/posts/<int:id>")
def posts_id(id):
    article = Article.query.get(id)  # обращаемся к таблице бд и сортируем по дате
    return render_template("posts_id.html", article=article)


@app.route("/posts/<int:id>/del")  # удаляем комментарий
def post_gelit(id):
    article = Article.query.get_or_404(id)  # обращаемся к таблице бд
    try:
        db.session.delete(article)  # удаляем запись из бд
        db.session.commit()  # созхраняем в бд
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])  # редактируем комментарий
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()  # созхраняем в бд
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)  # добавляем в бд
            db.session.commit()  # созхраняем в бд
            return redirect('/posts')
        except:
            return "При добавлении статьи произошла ошибка"
    else:
        return render_template("create-article.html")


# @app.route("/user/<string:name>/<int:number>")     # забираем имя из урла
# def user(name, number):
#    return "<rb><h3>USER PAGE:</h3>" + name + str(number)


if __name__ == "__main__":
    app.run(debug=False)
