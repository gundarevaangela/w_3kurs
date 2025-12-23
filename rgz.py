from flask import Blueprint, render_template, request, redirect, flash
from db import db
from db.models import users, initiatives, votes
from flask_login import login_required, current_user
from datetime import datetime
import random
from datetime import timedelta

rgz = Blueprint('rgz', __name__)

# ГЛАВНАЯ СТРАНИЦА
@rgz.route('/rgz/')
def main():
    page = request.args.get('page', 1, type=int)
    
    # Пагинация - 20 инициатив на страницу
    initiatives_list = initiatives.query.filter_by(is_active=True)\
        .order_by(initiatives.created_at.desc())\
        .paginate(page=page, per_page=20, error_out=False)
    
    # Считаем голоса для каждой инициативы
    for initiative in initiatives_list.items:
        upvotes = votes.query.filter_by(initiative_id=initiative.id, vote_type='up').count()
        downvotes = votes.query.filter_by(initiative_id=initiative.id, vote_type='down').count()
        initiative.score = upvotes - downvotes
    
    return render_template("rgz/index.html", initiatives=initiatives_list)

# СОЗДАНИЕ НОВОЙ ИНИЦИАТИВЫ
@rgz.route('/rgz/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('rgz/create.html')
    
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()
    
    # Проверка на пустые поля
    if not title:
        flash('Название не может быть пустым', 'error')
        return render_template('rgz/create.html')
    
    if not content:
        flash('Текст инициативы не может быть пустым', 'error')
        return render_template('rgz/create.html')
    
    try:
        new_initiative = initiatives(
            title=title,
            content=content,
            user_id=current_user.id,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_initiative)
        db.session.commit()
        
        return redirect(f'/rgz/initiative/{new_initiative.id}')
        
    except Exception:
        db.session.rollback()
        flash('Ошибка при создании инициативы', 'error')
        return render_template('rgz/create.html')

# ПРОСМОТР ИНИЦИАТИВЫ
@rgz.route('/rgz/initiative/<int:id>')
def view_initiative(id):
    initiative = initiatives.query.get_or_404(id)
    
    if not initiative.is_active:
        return redirect('/rgz/')
    
    # Считаем голоса
    upvotes = votes.query.filter_by(initiative_id=id, vote_type='up').count()
    downvotes = votes.query.filter_by(initiative_id=id, vote_type='down').count()
    score = upvotes - downvotes
    
    # Проверяем, голосовал ли текущий пользователь
    user_vote = None
    if current_user.is_authenticated:
        vote = votes.query.filter_by(user_id=current_user.id, initiative_id=id).first()
        if vote:
            user_vote = vote.vote_type
    
    return render_template('rgz/initiative.html',
                         initiative=initiative,
                         upvotes=upvotes,
                         downvotes=downvotes,
                         score=score,
                         user_vote=user_vote)

# ГОЛОСОВАНИЕ
@rgz.route('/rgz/vote/<int:id>', methods=['POST'])
@login_required
def vote(id):
    initiative = initiatives.query.get_or_404(id)
    vote_type = request.form.get('vote_type')
    
    if not initiative.is_active:
        return redirect('/rgz/')
    
    if initiative.user_id == current_user.id:
        flash('Нельзя голосовать за свою инициативу', 'error')
        return redirect(f'/rgz/initiative/{id}')
    
    if vote_type not in ['up', 'down']:
        return redirect(f'/rgz/initiative/{id}')
    
    try:
        # Проверяем существующий голос
        existing_vote = votes.query.filter_by(user_id=current_user.id, initiative_id=id).first()
        
        if existing_vote:
            if existing_vote.vote_type == vote_type:
                # Удаляем голос, если тот же тип
                db.session.delete(existing_vote)
            else:
                # Меняем голос
                existing_vote.vote_type = vote_type
        else:
            # Новый голос
            new_vote = votes(user_id=current_user.id, initiative_id=id, vote_type=vote_type)
            db.session.add(new_vote)
        
        db.session.commit()
        
        # Проверяем оценку для автоматического удаления
        check_initiative_score(id)
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при голосовании: {str(e)}', 'error')
    
    return redirect(f'/rgz/initiative/{id}')

# Функция проверки оценки
def check_initiative_score(initiative_id):
    initiative = initiatives.query.get(initiative_id)
    if not initiative or not initiative.is_active:
        return
    
    upvotes = votes.query.filter_by(initiative_id=initiative_id, vote_type='up').count()
    downvotes = votes.query.filter_by(initiative_id=initiative_id, vote_type='down').count()
    score = upvotes - downvotes
    
    if score < -10:
        initiative.is_active = False
        db.session.commit()

# УДАЛЕНИЕ СВОЕЙ ИНИЦИАТИВЫ
@rgz.route('/rgz/delete/<int:id>', methods=['POST'])
@login_required
def delete_initiative(id):
    initiative = initiatives.query.get_or_404(id)
    
    if initiative.user_id != current_user.id:
        return redirect(f'/rgz/initiative/{id}')
    
    try:
        # Сначала удаляем все голоса за эту инициативу
        votes.query.filter_by(initiative_id=id).delete()
        
        # Затем удаляем саму инициативу
        db.session.delete(initiative)
        db.session.commit()
        
        flash('Ваша инициатива успешно удалена', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении инициативы: {str(e)}', 'error')
    
    return redirect('/rgz/profile')

# ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ
@rgz.route('/rgz/profile')
@login_required
def profile():
    # Инициативы пользователя
    user_initiatives = initiatives.query.filter_by(
        user_id=current_user.id
    ).order_by(initiatives.created_at.desc()).all()
    
    # Считаем голоса для каждой инициативы
    for initiative in user_initiatives:
        upvotes = votes.query.filter_by(initiative_id=initiative.id, vote_type='up').count()
        downvotes = votes.query.filter_by(initiative_id=initiative.id, vote_type='down').count()
        initiative.score = upvotes - downvotes
    
    return render_template('rgz/profile.html', initiatives=user_initiatives)

# ========== АДМИНИСТРАТОР ==========

# АДМИН - УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ
@rgz.route('/rgz/admin/users')
@login_required
def admin_users():
    if not current_user.is_admin:
        return redirect('/rgz/')
    
    users_list = users.query.order_by(users.id).all()
    return render_template('rgz/admin_users.html', users=users_list)

# АДМИН - УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
@rgz.route('/rgz/admin/delete_user/<int:id>', methods=['POST'])
@login_required
def admin_delete_user(id):
    if not current_user.is_admin:
        return redirect('/rgz/')
    
    if id == current_user.id:
        flash('Нельзя удалить себя', 'error')
        return redirect('/rgz/admin/users')
    
    try:
        user = users.query.get_or_404(id)
        
        # 1. Находим все инициативы пользователя
        user_initiatives = initiatives.query.filter_by(user_id=id).all()
        
        # 2. Для каждой инициативы удаляем связанные голоса
        for initiative in user_initiatives:
            votes.query.filter_by(initiative_id=initiative.id).delete()
        
        # 3. Удаляем инициативы пользователя
        initiatives.query.filter_by(user_id=id).delete()
        
        # 4. Удаляем голоса, где пользователь голосовал
        votes.query.filter_by(user_id=id).delete()
        
        # 5. Удаляем самого пользователя
        db.session.delete(user)
        db.session.commit()
        
        flash(f'Пользователь {user.login} успешно удалён', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении пользователя: {str(e)}', 'error')
    
    return redirect('/rgz/admin/users')

# АДМИН - УПРАВЛЕНИЕ ИНИЦИАТИВАМИ
@rgz.route('/rgz/admin/initiatives')
@login_required
def admin_initiatives():
    if not current_user.is_admin:
        return redirect('/rgz/')
    
    initiatives_list = initiatives.query.order_by(initiatives.created_at.desc()).all()
    
    # Считаем голоса для каждой инициативы
    for initiative in initiatives_list:
        upvotes = votes.query.filter_by(initiative_id=initiative.id, vote_type='up').count()
        downvotes = votes.query.filter_by(initiative_id=initiative.id, vote_type='down').count()
        initiative.score = upvotes - downvotes
    
    return render_template('rgz/admin_initiatives.html', initiatives=initiatives_list)

# АДМИН - УДАЛЕНИЕ ИНИЦИАТИВЫ
@rgz.route('/rgz/admin/delete_initiative/<int:id>', methods=['POST'])
@login_required
def admin_delete_initiative(id):
    if not current_user.is_admin:
        return redirect('/rgz/')
    
    try:
        initiative = initiatives.query.get_or_404(id)
        
        # Сначала удаляем все голоса за эту инициативу
        votes.query.filter_by(initiative_id=id).delete()
        
        # Затем удаляем саму инициативу
        db.session.delete(initiative)
        db.session.commit()
        
        flash(f'Инициатива "{initiative.title}" успешно удалена', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Ошибка при удалении инициативы: {str(e)}', 'error')
    
    return redirect('/rgz/admin/initiatives')

# ИНИЦИАЛИЗАЦИЯ БД (создание администратора и тестовых инициатив)
@rgz.route('/rgz/init_db')
def init_db():
    try:
        # Проверяем, есть ли администратор
        admin = users.query.filter_by(login='admin').first()
        if not admin:
            return 'Для инициализации базы данных сначала зарегистрируйте пользователя admin через /lab8/register/'
        
        # Делаем администратором
        admin.is_admin = True
        db.session.commit()
        
        # Создаем тестовые инициативы
        if initiatives.query.count() < 100:
            # Все пользователи
            all_users = users.query.all()
            
            if not all_users:
                return 'Нет пользователей для создания инициатив'
            
            topics = [
                "Замена мышек в аудиториях",
                "Настройка и ремонт лифтов ФБ",
                "Парковочные места для студентов",
                "Улучшение столовой",
                "Библиотека 24/7",
                "Спортивная площадка",
                "Коворкинг зона",
                "Онлайн-курсы",
                "Экологические проекты",
                "Студенческие клубы"
            ]
            
            contents = [
                "Предлагаю заменить мышки во всех терминальных аудиториях ФБ, которые уже разваливаются в руках студентов.",
                "Необходимо настроить лифты так, чтобы они не переставали работать в час-пик.",
                "Предлагаю выделить парковочные места для студентов на территории вуза.",
                "Необходимо увеличить партию слоек с ветчиной и сыром.",
                "Предлагаю сделать библиотеку доступной круглосуточно во время сессии.",
                "Нужно построить новую спортивную площадку за общежитием №3.",
                "Создание коворкинг зоны для групповой работы студентов.",
                "Разработка онлайн-курсов по дополнительным дисциплинам.",
                "Организация раздельного сбора мусора в университете.",
                "Создание новых студенческих клубов по интересам."
            ]
            
            for i in range(100):
                author = random.choice(all_users)
                days_ago = random.randint(0, 365)
                created_at = datetime.utcnow() - timedelta(days=days_ago)
                
                initiative = initiatives(
                    title=f'{random.choice(topics)} #{i+1}',
                    content=f'{random.choice(contents)} Это предложение по улучшению условий в университете. #{i+1}',
                    user_id=author.id,
                    created_at=created_at,
                    is_active=random.choice([True, True, True, True, False])  # 80% активных
                )
                db.session.add(initiative)
            
            db.session.commit()
            
            # Создаем тестовые голоса
            all_initiatives = initiatives.query.all()
            for initiative in all_initiatives[:50]:  # Для первых 50 инициатив
                voters = random.sample(all_users, min(10, len(all_users)))
                for voter in voters:
                    if voter.id != initiative.user_id:  # Нельзя голосовать за свою инициативу
                        vote_type = random.choice(['up', 'down', 'up', 'up'])  # 75% за, 25% против
                        vote = votes(
                            user_id=voter.id,
                            initiative_id=initiative.id,
                            vote_type=vote_type
                        )
                        db.session.add(vote)
            
            db.session.commit()
        
        return '''
        ✅ База данных инициализирована!<br>
        • Пользователь admin теперь администратор<br>
        • Создано 100 тестовых инициатив<br>
        • Созданы тестовые голоса<br>
        <a href="/rgz/">Перейти на главную</a>
        '''
        
    except Exception as e:
        return f'❌ Ошибка: {str(e)}'