from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    list_of_articles = Article.query.order_by(Article.date).all()
    return render_template('articles.html', articles=list_of_articles)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/articles')
        except:
            return "Error while adding new article"
    else:
        return render_template('create-article.html')


@app.route('/articles/<int:articleid>')
def article_details(articleid):
    article = Article.query.get(articleid)
    return render_template('article-detail.html', article=article)


@app.route('/articles/<int:articleid>/delete')
def delete_article(articleid):
    article = Article.query.get_or_404(articleid)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/articles')
    except:
        return "Error while deleting article"


@app.route('/articles/<int:articleid>/update', methods=['POST', 'GET'])
def update_article(articleid):
    article = Article.query.get(articleid)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/articles')
        except:
            return "Error while updating article"
    else:
        return render_template('update-article.html', article=article)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
