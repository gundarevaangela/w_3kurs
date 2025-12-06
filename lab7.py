from flask import Blueprint, render_template, request, abort

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