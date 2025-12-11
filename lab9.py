from flask import Blueprint, render_template, request, jsonify, session, redirect
from db import db
from db.models import gift_box

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    boxes = gift_box.query.all()
    unopened_count = gift_box.query.filter_by(is_opened=False).count()

    if 'opened_count' not in session:
        session['opened_count'] = 0

    return render_template('lab9/index.html',
                           boxes=boxes,
                           unopened_count=unopened_count)


@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    data = request.get_json()
    box_id = data.get('box_id')

    box = gift_box.query.get(box_id)
    if not box:
        return jsonify({'error': 'not found'}), 404

    if box.is_opened:
        return jsonify({'already_opened': True})

    if 'opened_count' not in session:
        session['opened_count'] = 0

    if session['opened_count'] >= 3:
        return jsonify({'limit_exceeded': True})

    box.is_opened = True
    db.session.commit()

    session['opened_count'] += 1

    return jsonify({'success': True,
                    'redirect_url': f'/lab9/congratulation/{box_id}'})


@lab9.route('/lab9/congratulation/<int:box_id>')
def congratulation(box_id):
    box = gift_box.query.get(box_id)
    img_path = f'/static/lab9/congratulation_{box_id}.jpg'
    return render_template('lab9/congratulation.html',
                           img_path=img_path,
                           message=box.message)


@lab9.route('/lab9/init')
def init_boxes():
    # Удаляем старые записи
    gift_box.query.delete()
    
    # Добавляем 10 новогодних коробок с явными ID от 1 до 10
    boxes = [
      
        gift_box(id=1, pos_top=80, pos_left=300, message="🎄 С Новым 2026 годом! Пусть он принесет много счастья и радости!"),
        gift_box(id=2, pos_top=80, pos_left=600, message="🎅 Желаю, чтобы все мечты сбылись в новом году!"),
        gift_box(id=3, pos_top=80, pos_left=1100, message="🦌 Пусть 2026 год будет полон удивительных событий и открытий!"),
        gift_box(id=4, pos_top=80, pos_left=1700, message="❄️ Здоровья, тепла и уюта в новом году!"),
        gift_box(id=5, pos_top=280, pos_left=450, message="🌟 Пусть каждый день 2026 года будет светлым и радостным!"),
        gift_box(id=6, pos_top=280, pos_left=850, message="🎁 Желаю финансового благополучия и стабильности в 2026!"),
        gift_box(id=7, pos_top=280, pos_left=1400, message="🍾 Пусть новый год принесет только хорошие новости!"),
        gift_box(id=8, pos_top=280, pos_left=2000, message="🔥 Успехов в учебе и карьерного роста в новом году!"),
        gift_box(id=9, pos_top=480, pos_left=600, message="❤️ Любви, взаимопонимания и гармонии в 2026 году!"),
        gift_box(id=10, pos_top=480, pos_left=1600, message="🎇 Счастливого Нового года! Пусть он будет волшебным!")
    ]
    
    for box in boxes:
        db.session.add(box)
    
    db.session.commit()
    return "✅ База данных инициализирована с 10 новогодними коробками (ID 1-10). <br><br> <a href='/lab9/'>🎄 Перейти к новогодним подаркам 🎄</a>"

@lab9.route('/lab9/reset')
def reset_count():
    # Сбрасываем счетчик открытых подарков
    session['opened_count'] = 0
    
    # Также можно сбросить статус открытых коробок (опционально)
    boxes = gift_box.query.all()
    for box in boxes:
        box.is_opened = False
    db.session.commit()
    
    return redirect('/lab9/')