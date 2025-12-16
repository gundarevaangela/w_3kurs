from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import current_user, login_required
from db import db
from db.models import gift_box, user_opened_gifts
from datetime import datetime

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    # Получаем все коробки
    all_boxes = gift_box.query.all()
    
    # Фильтруем коробки в зависимости от авторизации
    if current_user.is_authenticated:
        boxes = all_boxes  # Показываем все коробки
        unopened_count = gift_box.query.filter_by(is_opened=False).count()
    else:
        # Для неавторизованных показываем только те, где requires_auth=False
        boxes = [b for b in all_boxes if not b.requires_auth]
        unopened_count = gift_box.query.filter_by(is_opened=False, requires_auth=False).count()
    
    # Считаем открытые подарки
    if current_user.is_authenticated:
        opened_count = user_opened_gifts.query.filter_by(user_id=current_user.id).count()
    else:
        if 'opened_count' not in session:
            session['opened_count'] = 0
        opened_count = session['opened_count']
    
    return render_template('lab9/index.html',
                           boxes=boxes,
                           unopened_count=unopened_count,
                           opened_count=opened_count,
                           is_authenticated=current_user.is_authenticated,
                           current_user=current_user)


@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    data = request.get_json()
    box_id = data.get('box_id')
    
    box = gift_box.query.get(box_id)
    if not box:
        return jsonify({'error': 'not found'}), 404
    
    # Проверка на необходимость авторизации
    if box.requires_auth and not current_user.is_authenticated:
        return jsonify({
            'auth_required': True, 
            'message': 'Этот особый подарок доступен только авторизованным пользователям!'
        })
    
    if box.is_opened:
        return jsonify({'already_opened': True})
    
    # Проверка лимита открытий (максимум 3)
    if current_user.is_authenticated:
        # Для авторизованных пользователей
        user_opened = user_opened_gifts.query.filter_by(user_id=current_user.id).all()
        opened_count = len(user_opened)
        if opened_count >= 3:
            return jsonify({'limit_exceeded': True})
    else:
        # Для неавторизованных пользователей
        if 'opened_count' not in session:
            session['opened_count'] = 0
        if session['opened_count'] >= 3:
            return jsonify({'limit_exceeded': True})
    
    # Отмечаем коробку как открытую
    box.is_opened = True
    
    # Сохраняем информацию об открытии
    if current_user.is_authenticated:
        user_gift = user_opened_gifts(user_id=current_user.id, gift_id=box.id)
        db.session.add(user_gift)
    else:
        session['opened_count'] = session.get('opened_count', 0) + 1
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'redirect_url': f'/lab9/congratulation/{box_id}'
    })


@lab9.route('/lab9/congratulation/<int:box_id>')
def congratulation(box_id):
    box = gift_box.query.get(box_id)
    if not box:
        return "Подарок не найден", 404
    
    img_path = f'/static/lab9/congratulation_{box_id}.jpg'
    
    # Считаем открытые подарки
    if current_user.is_authenticated:
        opened_count = user_opened_gifts.query.filter_by(user_id=current_user.id).count()
        remaining = max(0, 3 - opened_count)
    else:
        opened_count = session.get('opened_count', 0)
        remaining = max(0, 3 - opened_count)
    
    return render_template('lab9/congratulation.html',
                           img_path=img_path,
                           message=box.message,
                           opened_count=opened_count,
                           remaining=remaining,
                           is_authenticated=current_user.is_authenticated,
                           box_id=box_id)


@lab9.route('/lab9/init')
def init_boxes():
    try:
        # Важно: сначала удаляем записи в user_opened_gifts, потом в gift_box
        user_opened_gifts.query.delete()  # Удаляем сначала дочерние записи
        gift_box.query.delete()           # Потом родительские записи
        
        # Создаем 10 коробок (среди них 3 особых, требующих авторизации)
        boxes = [
            # Обычные подарки (не требуют авторизации) - 7 штук
            gift_box(id=1, pos_top=80, pos_left=300, requires_auth=False,
                     message="🎄 С Новым 2026 годом! Пусть он принесет много счастья и радости!"),
            gift_box(id=2, pos_top=80, pos_left=650, requires_auth=False,
                     message="🎅 Желаю, чтобы все мечты сбылись в новом году!"),
            gift_box(id=3, pos_top=80, pos_left=1100, requires_auth=False,
                     message="🦌 Пусть 2026 год будет полон удивительных событий и открытий!"),
            gift_box(id=4, pos_top=80, pos_left=1700, requires_auth=False,
                     message="❄️ Здоровья, тепла и уюта в новом году!"),
            gift_box(id=5, pos_top=280, pos_left=450, requires_auth=False,
                     message="🌟 Пусть каждый день 2026 года будет светлым и радостным!"),
            gift_box(id=6, pos_top=280, pos_left=850, requires_auth=False,
                     message="🎁 Желаю финансового благополучия и стабильности в 2026!"),
            gift_box(id=7, pos_top=280, pos_left=1400, requires_auth=False,
                     message="🍾 Пусть новый год принесет только хорошие новости!"),
            
            # Особые подарки (требуют авторизации) - 3 штуки
            gift_box(id=8, pos_top=290, pos_left=1200, requires_auth=True,
                     message="🔥 ОСОБЫЙ ПОДАРОК: Успехов в учебе и карьерного роста! Только для авторизованных!"),
            gift_box(id=9, pos_top=350, pos_left=600, requires_auth=True,
                     message="❤️ ОСОБЫЙ ПОДАРОК: Любви, взаимопонимания и гармонии! Только для авторизованных!"),
            gift_box(id=10, pos_top=150, pos_left=1800, requires_auth=True,
                     message="🎇 ОСОБЫЙ ПОДАРОК: Счастливого Нового года! Пусть он будет волшебным! Только для авторизованных!")
        ]
        
        for box in boxes:
            db.session.add(box)
        
        db.session.commit()
        
        return """
        ✅ База данных инициализирована с 10 коробками:<br>
        • 7 обычных подарков (доступны всем)<br>
        • 3 особых подарка (только для авторизованных)<br><br>
        <a href='/lab9/' style='font-size: 18px; padding: 10px 20px; background: #c2185b; color: white; text-decoration: none; border-radius: 5px;'>
            🎄 Перейти к новогодним подаркам 🎄
        </a>
        """
    
    except Exception as e:
        db.session.rollback()
        return f"❌ Ошибка при инициализации: {str(e)}<br><br><a href='/lab9/'>Вернуться назад</a>", 500


@lab9.route('/lab9/reset', methods=['POST'])
@login_required
def reset_boxes():
    try:
        # Сбрасываем статус всех коробок
        boxes = gift_box.query.all()
        for box in boxes:
            box.is_opened = False
        
        # Удаляем записи об открытых подарках для текущего пользователя
        user_opened_gifts.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '🎅 Дед Мороз наполнил все коробки заново!'
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Ошибка: {str(e)}'
        }), 500


@lab9.route('/lab9/reset_session')
def reset_session():
    """Сброс сессии для неавторизованных пользователей"""
    session['opened_count'] = 0
    return redirect(url_for('lab9.main'))