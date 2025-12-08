from flask import Blueprint, render_template, request, abort
from datetime import datetime
lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Shutter Island",
        "title_ru": "Остров проклятых",
        "year": 2009,
        "description": "Два американских судебных пристава отправляются на один из островов в штате Массачусетс, "
        "чтобы расследовать исчезновение пациентки клиники для умалишенных преступников. При проведении расследования"
        "им придется столкнуться с паутиной лжи, обрушившимся ураганом и смертельным бунтом обитателей клиники."
    },
    {
        "title": "Léon",
        "title_ru": "Леон",
        "year": 1994,
        "description": "Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней"
        " соседке Матильде, семью которой убили коррумпированные полицейские"
    },
    {
        "title": "The Fifth Element",
        "title_ru": "Пятый элемент",
        "year": 1997,
        "description": "2257 год. Бывший секретный агент Корбен Даллас работает таксистом,"
        "ест в одном и том же ресторане и не ждёт перемен от жизни. Всё меняется, когда в его такси"
        "падает инопланетянка Лилу — единственное существо, способное спасти человечество. Вместе им "
        "предстоит остановить надвигающееся зло и предотвратить межгалактическую войну."
    },
]

def validate_film(film):
    """Валидация всех полей фильма"""
    errors = {}
    
    # Проверка русского названия (обязательное поле)
    title_ru = film.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Заполните русское название'
    
    # Проверка оригинального названия
    title = film.get('title', '').strip()
    if not title and not title_ru:
        # Если оба названия пустые
        errors['title'] = 'Заполните название на оригинальном языке'
    elif not title:
        # Если оригинальное пустое, а русское есть - копируем русское
        film['title'] = title_ru
    
    # Проверка года
    year = film.get('year')
    if year is None or year == '':
        errors['year'] = 'Заполните год выпуска'
    else:
        try:
            # Преобразуем в число
            year_int = int(year)
            current_year = datetime.now().year
            if year_int < 1895 or year_int > current_year:
                errors['year'] = f'Год должен быть от 1895 до {current_year}'
            else:
                # Сохраняем как число
                film['year'] = year_int
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    
    film = request.get_json()
    if film is None:
        return {'error': 'Invalid JSON'}, 400
    
    # Валидация всех полей
    errors = validate_film(film)
    if errors:
        return errors, 400
    
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film is None:
        return {'error': 'Invalid JSON'}, 400
    
    # Валидация всех полей
    errors = validate_film(film)
    if errors:
        return errors, 400
    
    films.append(film)
    return {'id': len(films) - 1}, 201