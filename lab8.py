from flask import Blueprint, request, redirect, render_template, flash, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy.exc import IntegrityError

lab8 = Blueprint('lab8', __name__)

# ГЛАВНАЯ СТРАНИЦА 
@lab8.route("/lab8/")
def lab():
    login = current_user.login if current_user.is_authenticated else None
    return render_template('lab8/lab8.html', login=login)

# РЕГИСТРАЦИЯ 
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('lab8/register.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не должен быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    try:
        password_hash = generate_password_hash(password_form)
        new_user = users(login=login_form, password=password_hash)

        db.session.add(new_user)
        db.session.commit()

        # Автоматический логин после регистрации
        login_user(new_user, remember=False)
        return redirect('/lab8/')
    except IntegrityError as e:
        db.session.rollback()
        return render_template('lab8/register.html', error=f'Ошибка при регистрации: {e}')
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/register.html', error=f'Произошла неизвестная ошибка: {e}')

# ВХОД 
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = False
    if request.form.get('remember'):
        remember_me = True

    if not login_form:
        return render_template('lab8/login.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('lab8/login.html', error='Пароль не должен быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

# ВЫХОД 
@lab8.route('/lab8/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# ЛИЧНЫЕ СТАТЬИ (персональный кабинет с поиском)
@lab8.route('/lab8/personal_articles/')
@login_required
def personal_articles():
    search_query = request.args.get('search')  # Получаем строку поиска
    if search_query:
        articles_list = articles.query.filter(
            articles.login_id == current_user.id,
            articles.title.ilike(f'%{search_query}%')
        ).all()
    else:
        articles_list = current_user.articles  # Доступ к статьям через relationship
    
    return render_template('lab8/personal_articles.html', articles=articles_list)

# ПУБЛИЧНЫЕ СТАТЬИ 
@lab8.route('/lab8/public_articles/')
def public_articles():
    search_query = request.args.get('search')  # Получаем строку поиска
    if search_query:
        public_articles_list = articles.query.filter(
            articles.is_public == True,
            articles.title.ilike(f'%{search_query}%')
        ).all()
    else:
        public_articles_list = articles.query.filter_by(is_public=True).all()
    
    return render_template('lab8/public_articles.html', articles=public_articles_list)

# СПИСОК СТАТЕЙ (с управлением публикацией)
@lab8.route('/lab8/articles', methods=['GET', 'POST'])
@login_required
def list_articles():
    status_message = None
    
    if request.method == 'POST':
        article_id = request.form.get('article_id')
        is_public = request.form.get('is_public') == 'on'
        
        article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
        if article:
            article.is_public = is_public
            db.session.commit()
            status_message = f"Статус статьи «{article.title}» обновлен."
        else:
            status_message = "Ошибка: статья не найдена или недоступна."
    
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/list_articles.html', 
                          articles=user_articles, 
                          status_message=status_message)

# СОЗДАНИЕ СТАТЬИ 
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_public = request.form.get('is_public') == 'on'
    
    # Валидация пустых полей
    if not title or not article_text:
        return render_template('lab8/create_article.html', error='Название и текст статьи не могут быть пустыми.')
    
    try:
        new_article = articles(
            login_id=current_user.id,
            title=title,
            article_text=article_text,
            is_favorite=False,
            is_public=is_public,
            likes=0
        )
        
        db.session.add(new_article)
        db.session.commit()
        return redirect('/lab8/personal_articles')
    except IntegrityError as e:
        db.session.rollback()
        return render_template('lab8/create_article.html', error=f'Ошибка при создании статьи: {e}')
    except Exception as e:
        db.session.rollback()
        return render_template('lab8/create_article.html', error=f'Произошла неизвестная ошибка: {e}')

# РЕДАКТИРОВАНИЕ СТАТЬИ 
@lab8.route('/lab8/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    article = articles.query.get_or_404(id)
    
    # Проверка, является ли текущий пользователь автором статьи
    if article.login_id != current_user.id:
        flash('У Вас нет прав на редактирование этой статьи.', 'error')
        return redirect(url_for('lab8.personal_articles'))
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    
    # Валидация: проверяем, что поля не пустые
    if not title or not article_text:
        return render_template('lab8/edit_article.html', 
                              article=article, 
                              error='Название и текст статьи не могут быть пустыми.')
    
    # Обновляем поля статьи
    article.title = title
    article.article_text = article_text
    db.session.commit()
    
    return redirect(url_for('lab8.personal_articles'))

# АЛЬТЕРНАТИВНЫЙ МАРШРУТ ДЛЯ РЕДАКТИРОВАНИЯ
@lab8.route('/lab8/article/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if not article:
        return redirect('/lab8/articles')
    
    if request.method == 'POST':
        title = request.form.get('title')
        text = request.form.get('text')
        
        if not title or not text:
            return render_template('lab8/edit_article.html',
                                  article=article,
                                  error="Название и текст статьи не могут быть пустыми.")
        
        article.title = title
        article.article_text = text
        db.session.commit()
        return redirect('/lab8/articles')
    
    return render_template('lab8/edit_article.html', article=article)

# УДАЛЕНИЕ СТАТЬИ 
@lab8.route('/lab8/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    article = articles.query.get_or_404(id)
    
    # Проверка, является ли текущий пользователь автором статьи
    if article.login_id != current_user.id:
        flash('У Вас нет прав на удаление этой статьи.', 'error')
        return redirect(url_for('lab8.personal_articles'))
    
    db.session.delete(article)
    db.session.commit()
    
    flash('Статья успешно удалена.', 'success')
    return redirect(url_for('lab8.personal_articles'))

# АЛЬТЕРНАТИВНЫЙ МАРШРУТ ДЛЯ УДАЛЕНИЯ
@lab8.route('/lab8/article/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.filter_by(id=article_id, login_id=current_user.id).first()
    
    if article:
        db.session.delete(article)
        db.session.commit()
        flash('Статья успешно удалена.', 'success')
    
    return redirect('/lab8/articles')

# ПЕРЕКЛЮЧЕНИЕ ИЗБРАННОГО 
@lab8.route('/lab8/toggle_favorite/<int:id>', methods=['POST'])
@login_required
def toggle_favorite(id):
    article = articles.query.get_or_404(id)
    
    # Проверка прав доступа
    if article.login_id != current_user.id:
        flash('У Вас нет прав на изменение этой статьи.', 'error')
        return redirect(url_for('lab8.personal_articles'))
    
    # Инвертируем состояние is_favorite
    article.is_favorite = not article.is_favorite
    db.session.commit()
    
    return redirect(url_for('lab8.personal_articles'))

# ПЕРЕКЛЮЧЕНИЕ ПУБЛИЧНОСТИ 
@lab8.route('/lab8/toggle_public/<int:id>', methods=['POST'])
@login_required
def toggle_public(id):
    article = articles.query.get_or_404(id)
    
    # Проверка прав доступа
    if article.login_id != current_user.id:
        flash('У Вас нет прав на изменение этой статьи.', 'error')
        return redirect(url_for('lab8.personal_articles'))
    
    # Инвертируем состояние is_public
    article.is_public = not article.is_public
    db.session.commit()
    
    return redirect(url_for('lab8.personal_articles'))

# ЛАЙК СТАТЬИ 
@lab8.route('/lab8/like_article/<int:id>', methods=['POST'])
def like_article(id):
    article = articles.query.get_or_404(id)
    
    # Проверяем, публичная ли статья
    if not article.is_public:
        flash('Эта статья не публичная.', 'error')
        return redirect(url_for('lab8.public_articles'))
    
    # Инвертируем состояние лайка (1 - лайк, 0 - нет лайка)
    article.likes = 1 if article.likes == 0 else 0
    db.session.commit()
    
    return redirect(url_for('lab8.public_articles'))