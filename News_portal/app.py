from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from forms import NewsForm, SearchForm

# Инициализация объектов приложения и расширений
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db = SQLAlchemy(app)  # Передаем app напрямую в SQLAlchemy
login_manager = LoginManager(app)  # Передаем app напрямую в LoginManager

@login_manager.user_loader
def load_user(user_id):
    from models import User  # Импортируем User только здесь
    return User.query.get(int(user_id))

class NewsArticle(db.Model):  # Определяем модель NewsArticle
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # Поле для хранения даты

def create_app():
    # Инициализируем приложение
    with app.app_context():
        db.create_all()  # Создаем таблицы, если их еще нет

    return app

# Запрещенные слова для цензуры
censored_words = ['редиска', 'редиске', 'редиски', 'редиску']

def censor(text):
    if not isinstance(text, str):
        raise ValueError("filter censor должен применяться только к строкам")
    for word in censored_words:
        replacement = word[0] + '*' * (len(word) - 1)
        text = text.replace(word, replacement)
    return text

@app.route('/news/', methods=['GET'])
def news_list():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = NewsArticle.query.order_by(NewsArticle.date.desc()).paginate(page=page, per_page=per_page, error_out=False)
    articles = pagination.items
    return render_template('news_list.html', news=articles, pagination=pagination)

@app.route('/news/create/', methods=['GET', 'POST'])
@login_required  # Защита маршрута для авторизованных пользователей
def news_create():
    form = NewsForm()
    if form.validate_on_submit():
        new_article = NewsArticle(
            title=form.title.data,
            content=form.content.data,
            date=datetime.utcnow()  # Используем текущую дату
        )
        try:
            db.session.add(new_article)
            db.session.commit()
            flash('Статья успешно создана!', 'success')
            return redirect(url_for('news_list'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при создании статьи: {}'.format(str(e)), 'danger')
    return render_template('news_create.html', form=form)

@app.route('/news/<int:news_id>/edit/', methods=['GET', 'POST'])
@login_required  # Защита маршрута для авторизованных пользователей
def news_edit(news_id):
    article = NewsArticle.query.get_or_404(news_id)
    form = NewsForm(obj=article)
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        try:
            db.session.commit()
            flash('Статья успешно обновлена!', 'success')
            return redirect(url_for('news_detail', news_id=article.id))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при обновлении статьи: {}'.format(str(e)), 'danger')
    return render_template('news_edit.html', form=form, article=article)

@app.route('/news/<int:news_id>/delete/', methods=['GET', 'POST'])
@login_required  # Защита маршрута для авторизованных пользователей
def news_delete(news_id):
    article = NewsArticle.query.get_or_404(news_id)
    if request.method == 'POST':
        try:
            db.session.delete(article)
            db.session.commit()
            flash('Статья успешно удалена!', 'success')
            return redirect(url_for('news_list'))
        except Exception as e:
            db.session.rollback()
            flash('Ошибка при удалении статьи: {}'.format(str(e)), 'danger')
    return render_template('news_delete.html', article=article)

@app.route('/news/search', methods=['GET', 'POST'])
def news_search():
    form = SearchForm()
    articles = []
    if form.validate_on_submit():
        query = NewsArticle.query
        if form.title.data:
            query = query.filter(NewsArticle.title.contains(form.title.data))
        if form.date.data:
            query = query.filter(NewsArticle.date >= form.date.data)
        articles = query.all()
    return render_template('search.html', form=form, articles=articles)

@app.route('/news/<int:news_id>/', methods=['GET'])
def news_detail(news_id):
    article = NewsArticle.query.get_or_404(news_id)
    article.title = censor(article.title)
    article.content = censor(article.content)
    formatted_date = article.date.strftime('%d.%m.%Y')  # Форматируем дату
    return render_template('news_detail.html', article=article, date=formatted_date)

if __name__ == '__main__':
    create_app()  # Инициализируем приложение
    app.run(debug=True)  # Запускаем приложение в режиме отладки