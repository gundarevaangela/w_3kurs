
from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab2 = Blueprint('lab2' ,__name__)
@lab2.route('/lab2/a')
def a():
    return 'без слеша'
  

@lab2.route('/lab2/a/')
def a2():
    return 'со слешем'

flowers = [
    {"name": "роза", "price": 300},
    {"name": "тюльпан", "price": 250},
    {"name": "незабудка", "price": 150},
    {"name": "ромашка", "price": 200},
]


@lab2.route('/lab2/flowers/<int:flower_id>')
def id_flowers(flower_id):
    if flower_id >= len(flowers):
        abort(404)
    else:
        flower = list(flowers[flower_id].values())[0]
        return f'''
<!doctype html>
<html>
    <body>
        <h1>Вы выбрали Цветы</h1>
        <p>Ваш букет из: <b>{flower}</b></p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''
    

@lab2.route('/lab2/add_flower/<name>')
def add_flower(name):
    flowers.lab2end({"name": name, "price": 300})
    return redirect(url_for("all_flowers"))


@lab2.route('/lab2/add_flower/')
def add_flower_no_name():
    return "Вы не задали имя цветка", 400


@lab2.route('/lab2/all_flowers')
def all_flowers():
    return render_template("flowers.html", flowers=flowers)


@lab2.route("/lab2/del_flower/<int:flower_id>")
def del_flower(flower_id):
    if 0 <= flower_id < len(flowers):
        flowers.pop(flower_id)
        return redirect(url_for("all_flowers"))
    else:
        abort(404)


@lab2.route('/lab2/del_flower/')
def del_flower_no_name():
    return "Вы не задали имя цветка", 400


@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flowers.clear()
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список очищен</h1>
        <p>Все цветы.</p>
        <a href="/lab2/all_flowers">Посмотреть все цветы</a>
    </body>
</html>
'''


@lab2.route('/lab2/example')
def example():
    name = 'Gundareva Angela'
    num_lab = '2'
    group = 'FBI-31'
    num_kurs = '3'
    fruits = [
        {'name':'яблоки', 'price': 100},
        {'name':'груши', 'price': 120},
        {'name':'апельсины', 'price': 80},
        {'name':'мандарины', 'price': 95},
        {'name':'манго', 'price': 321},
    ]
    return render_template('example.html',
                        name=name,
                        num_lab=num_lab,
                        group=group,
                        num_kurs=num_kurs,
                        fruits=fruits)


@lab2.route('/lab2')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase = phrase)

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    result = f"""
<!doctype html>
<html>
    <body>
        <h1>Калькулятор</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} * {b} = {a * b}</p>
        <p>{a} / {b} = {"нельзя делить на 0" if b == 0 else a / b}</p>
        <p>{a} ** {b} = {a ** b}</p>
        <hr>
        <a href="/lab2">Назад к лабораторной 2</a>
    </body>
</html>
"""
    return result


@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calc_one_arg(a):
    return redirect(f'/lab2/calc/{a}/1')


books = [
    {"author": "Джоан Роулинг", "title": "Гарри Поттер и философский камень", "genre": "Фэнтези", "pages": 432},
    {"author": "Джон Р. Р. Толкин", "title": "Властелин колец: Братство кольца", "genre": "Фэнтези", "pages": 576},
    {"author": "Агата Кристи", "title": "Убийство в Восточном экспрессе", "genre": "Детектив", "pages": 320},
    {"author": "Стивен Кинг", "title": "Оно", "genre": "Ужасы", "pages": 1248},
    {"author": "Джейн Остин", "title": "Гордость и предубеждение", "genre": "Роман", "pages": 432},
    {"author": "Эрих Мария Ремарк", "title": "Три товарища", "genre": "Классика", "pages": 384},
    {"author": "Харуки Мураками", "title": "Норвежский лес", "genre": "Роман", "pages": 400},
    {"author": "Пауло Коэльо", "title": "Алхимик", "genre": "Философская проза", "pages": 256},
    {"author": "Дэн Браун", "title": "Код да Винчи", "genre": "Триллер", "pages": 480},
    {"author": "Маргарет Митчелл", "title": "Унесённые ветром", "genre": "Исторический роман", "pages": 1024},
    {"author": "Оскар Уайльд", "title": "Портрет Дориана Грея", "genre": "Классика", "pages": 320},
    {"author": "Фрэнсис Скотт Фицджеральд", "title": "Великий Гэтсби", "genre": "Классика", "pages": 256},
    {"author": "Габриэль Гарсия Маркес", "title": "Сто лет одиночества", "genre": "Магический реализм", "pages": 448},
    {"author": "Артур Конан Дойл", "title": "Приключения Шерлока Холмса", "genre": "Детектив", "pages": 384},
    {"author": "Антуан де Сент-Экзюпери", "title": "Маленький принц", "genre": "Философская сказка", "pages": 96}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)


chocolate_bars = [
    {"name": "Snickers", "desc": "Арахис, нуга, карамель и молочный шоколад. Самый популярный батончик в мире.", "image": "snickers.png"},
    {"name": "Mars", "desc": "Нуга, карамель и молочный шоколад. Классический вкус с 1932 года.", "image": "mars.jpg"},
    {"name": "Twix", "desc": "Хрустящее печенье с карамелью в молочном шоколаде. Выпускается в двух пальчиках.", "image": "twix.jpeg"},
    {"name": "Bounty", "desc": "Нежная кокосовая начинка в молочном или тёмном шоколаде. Райское наслаждение.", "image": "bounty.jpg"},
    {"name": "Milky Way", "desc": "Воздушная нуга и карамель в молочном шоколаде. Легкий и нежный вкус.", "image": "milkyway.jpg"},
    {"name": "KitKat", "desc": "Хрустящие вафельные слои в молочном шоколаде. Сломай и поделись с друзьями.", "image": "kitkat.jpg"},
    {"name": "Nuts", "desc": "Целый лесной орех в хрустящей вафле и молочном шоколаде.", "image": "nuts.jpg"},
    {"name": "Picnic", "desc": "Хрустящие рисовые шарики, арахис, карамель и молочный шоколад.", "image": "picnic.jpg"},
    {"name": "M&Ms", "desc": "Шоколадные драже в цветной сахарной глазури. Тают во рту, а не в руках.", "image": "mms.jpg"},
    {"name": "Kinder Chocolate", "desc": "Нежный молочный шоколад с молочной начинкой. Создан специально для детей.", "image": "kinder.jpg"},
    {"name": "Kinder Bueno", "desc": "Хрустящие вафли с лесным орехом и сливочным кремом в шоколаде.", "image": "bueno.jpeg"},
    {"name": "Kinder Joy", "desc": "Шоколадное яйцо с игрушкой внутри. Два удовольствия в одном.", "image": "joy.jpg"},
    {"name": "Ferrero Rocher", "desc": "Целый лесной орех в хрустящем вафельном шарике и молочном шоколаде.", "image": "ferrero.jpg"},
    {"name": "Raffaello", "desc": "Нежный кокосовый батончик с цельным миндалем внутри. Легкий и изысканный вкус.", "image": "raffaello.jpg"},
    {"name": "Toblerone", "desc": "Швейцарский шоколад с медом, нугой и миндалем в фирменной треугольной упаковке.", "image": "toblerone.jpg"},
    {"name": "Lion", "desc": "Хрустящие злаки, карамель и арахис в молочном шоколаде. Энергия льва.", "image": "lion.jpg"},
    {"name": "Wispa", "desc": "Воздушный пористый молочный шоколад. Невероятно нежная текстура.", "image": "wispa.png"},
    {"name": "Crunch", "desc": "Хрустящие рисовые шарики в молочном шоколаде. Уникальная текстура.", "image": "crunch.jpg"},
    {"name": "Alpen Gold", "desc": "Доступный шоколад российского производства с различными начинками.", "image": "alpengold.jpeg"},
    {"name": "Рот Фронт", "desc": "Легендарный российский батончик с различными начинками. Суфле, помадка, вафли.", "image": "rotfront.jpg"},
]

@lab2.route('/lab2/chocolate')
def chocolate():
    return render_template("chocolate.html", bars=chocolate_bars)