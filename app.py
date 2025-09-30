from flask import Flask, url_for, request, redirect, abort, render_template
import datetime
app = Flask(__name__)

# список логов
access_log = []
@app.errorhandler(404)
def not_found(err):
    osh = url_for("static", filename="404.jpeg") 


    user_ip = request.remote_addr
    access_time = str(datetime.datetime.now())
    requested_url = request.url

    # добавляем запись в журнал
    access_log.append(f"[{access_time}] пользователь {user_ip} зашёл на адрес: {requested_url}")

    log_html = "<ul>"
    for entry in reversed(access_log):  # последние записи сверху
        log_html += f"<li>{entry}</li>"
    log_html += "</ul>"


    return '''
<!doctype html>
<html>
    <head>
        <style>
            body {
                margin: 0;
                padding: 30px;
                background: linear-gradient(135deg, #ffe4ec 0%, #ffd1dc 50%, #ffc2d6 100%);
                font-family: 'Arial', sans-serif;
                color: #d63384;
                min-height: 100vh;
            }
            .container {
                max-width: 1000px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 10px 30px rgba(214, 51, 132, 0.2);
                border: 3px solid #ff9eb4;
            }
            h1 {
                color: #c2185b;
                font-size: 2.5em;
                text-align: center;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(194, 24, 91, 0.1);
            }
            h2 {
                color: #d63384;
                border-bottom: 2px solid #ffafc5;
                padding-bottom: 10px;
                margin-top: 30px;
            }
            .error-image {
                display: block;
                margin: 20px auto;
                max-width: 300px;
                border-radius: 15px;
                box-shadow: 0 6px 15px rgba(214, 51, 132, 0.25);
                border: 2px solid #ffafc5;
            }
            .info {
                background: linear-gradient(135deg, #ffe4ec 0%, #ffd1dc 100%);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                border: 2px solid #ffc2d6;
                font-size: 1.1em;
            }
            .log {
                background: rgba(255, 240, 245, 0.8);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                border: 2px solid #ffd6e7;
                max-height: 300px;
                overflow-y: auto;
            }
            .log ul {
                list-style: none;
                padding: 0;
                margin: 0;
            }
            .log li {
                background: rgba(255, 255, 255, 0.7);
                margin: 8px 0;
                padding: 12px;
                border-radius: 10px;
                border-left: 4px solid #ff85a2;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                color: #880e4f;
            }
            .log li:hover {
                background: rgba(255, 255, 255, 0.9);
                transform: translateX(5px);
                transition: all 0.3s ease;
            }
            a {
                color: #e91e63;
                text-decoration: none;
                font-weight: bold;
                padding: 12px 25px;
                background: rgba(255, 255, 255, 0.7);
                border-radius: 25px;
                display: inline-block;
                margin: 10px 5px;
                transition: all 0.3s ease;
                border: 2px solid #ffafc5;
            }
            a:hover {
                background: rgba(255, 255, 255, 0.9);
                transform: translateY(-2px);
                box-shadow: 0 4px 15px rgba(233, 30, 99, 0.2);
            }
            .home-button {
                background: linear-gradient(135deg, #ff4d94 0%, #d63384 100%) !important;
                color: white !important;
                padding: 15px 30px !important;
                font-size: 1.1em !important;
            }
            .home-button:hover {
                background: linear-gradient(135deg, #ff6fa9 0%, #e91e63 100%) !important;
            }
        </style>
    </head>
    <body>
       <h1>Ошибка 404 - Страница не найдена</h1>
       <p>Котик устал, попробуйте позже</p>
       <img src="''' + osh + '''">
        <div class="info">
            Ваш IP: '''+str(user_ip)+'''<br>
            Дата доступа: '''+access_time+'''<br>
            <a href="/">На главную</a>
        </div>
        <div class="log">
            <h2>Журнал посещений</h2>
            '''+log_html+'''
        </div>
       <br>
      
       
    </body>
</html>
''', 404



@app.route("/index")
@app.route("/")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #fff0f5 0%, #ffe4e6 50%, #fce7f3 100%); 
                text-align: center;
                min-height: 100vh;
            }
            header { 
                background: linear-gradient(135deg, #ff85a2 0%, #fb6f92 100%); 
                color: white; 
                padding: 25px; 
                text-align: center; 
                margin: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(251, 111, 146, 0.3);
            }
            a { 
                color: #d63384; 
                font-weight: bold;
                text-decoration: none;
                transition: all 0.3s ease;
                font-size: 35px;
                padding: 8px 15px;
            }
            a:hover { 
                color: #ff4d94;
                text-decoration: underline;
                transform: translateY(-2px);
                font-size: 30px;
            }
            .nav-link {
                font-size: 20px;
                margin: 0 15px;
                padding: 10px 20px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 25px;
                border: 2px solid #ffb3c6;
            }
            .nav-link:hover {
                background: rgba(255, 255, 255, 0.5);
                font-size: 21px;
            }
            footer { 
                background: linear-gradient(135deg, #ffd6e7 0%, #ffc2d6 100%); 
                text-align: center; 
                padding: 15px; 
                position: fixed; 
                bottom: 0; 
                width: 100%;
                box-shadow: 0 -2px 10px rgba(214, 51, 132, 0.1);
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                padding: 25px;
                background: rgba(255, 255, 255, 0.9);
                border-radius: 20px;
                box-shadow: 0 8px 25px rgba(251, 111, 146, 0.15);
                margin-top: 20px;
                margin-bottom: 70px;
                backdrop-filter: blur(10px);
            }
            nav ul {
                list-style: none;
                padding: 0;
            }
            nav li {
                display: inline-block;
                margin: 0 20px;
            }
            .navigation {
                background: linear-gradient(135deg, #ffe4ec 0%, #ffd1dc 100%);
                padding: 20px;
                border-radius: 15px;
                margin: 25px 0;
                border: 2px solid #ffb3c6;
            }
            .navigation a {
                font-size: 22px;
                margin: 0 10px;
                padding: 12px 25px;
                background: rgba(255, 255, 255, 0.4);
                border-radius: 30px;
                display: inline-block;
            }
            .navigation a:hover {
                background: rgba(255, 255, 255, 0.7);
                font-size: 23px;
            }
            h1, h2, h3 {
                color: #c2185b;
                text-shadow: 1px 1px 2px rgba(194, 24, 91, 0.1);
            }
            p {
                color: #880e4f;
            }
            strong {
                color: #d63384;
            }
            hr {
                border: none;
                height: 2px;
                background: linear-gradient(90deg, transparent, #ff85a2, transparent);
                margin: 20px 0;
            }
            .main-link {
                font-size: 24px;
                padding: 15px 30px;
                background: linear-gradient(135deg, #ff4d94 0%, #d63384 100%);
                color: white !important;
                border-radius: 35px;
                margin: 20px;
                display: inline-block;
                box-shadow: 0 4px 15px rgba(214, 51, 132, 0.3);
            }
            .main-link:hover {
                background: linear-gradient(135deg, #ff6fa9 0%, #e91e63 100%);
                transform: translateY(-3px);
                box-shadow: 0 6px 20px rgba(214, 51, 132, 0.4);
                font-size: 25px;
            }
        </style>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        <nav>
            <a href="/lab1">Первая лабораторная</a>
        </nav>
        <footer>
            Гундарева Анжела, ФБИ-31, 3 курс, 2025
        </footer>
    </body>
</html>
'''
@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Лабораторная 1</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 20px; 
                background: linear-gradient(135deg, #fff0f5 0%, #ffe4e6 50%, #fce7f3 100%); 
                color: #880e4f; 
                line-height: 1.6
            }
            a { 
                color: #d63384; 
                font-weight: bold;
                text-decoration: none;
                font-size: 18px;
                transition: all 0.3s ease;
            }
            a:hover { 
                color: #ff4d94;
                text-decoration: underline;
                transform: translateY(-2px);
            }
        </style>
    </head>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор 
        инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков 
        — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <p><a href="/">На главную</a></p>
        

        <h2>Список роутов</h2>
        <ul>
            <li><a href="/index">/index</a></li>
            <li><a href="/">/</a></li>
            <li><a href="/lab1/web">/web</a></li>
            <li><a href="/lab1/author">/author</a></li>
            <li><a href="/lab1/image">/image</a></li>
            <li><a href="/lab1/counter">/counter</a></li>
            <li><a href="/lab1/counter/reset">/counter/reset</a></li>
            <li><a href="/lab1/info">/info</a></li>
            <li><a href="/lab1/created">/created</a></li>
            <li><a href="/lab1/error/400">/error/400</a></li>
            <li><a href="/lab1/error/401">/error/401</a></li>
            <li><a href="/lab1/error/402">/error/402</a></li>
            <li><a href="/lab1/error/403">/error/403</a></li>
            <li><a href="/lab1/error/405">/error/405</a></li>
            <li><a href="/lab1/error/418">/error/418</a></li>
            <li><a href="/lab1/cause_error">/cause_error</a></li>
        </ul>
    </body>
    </body>
</html>
'''



@app.route("/lab1/error/400")
def error_400():
    return "неверный запрос", 400

@app.route("/lab1/error/401")
def error_401():
    return "требуется авторизация", 401

@app.route("/lab1/error/402")
def error_402():
    return "требуется оплата", 402

@app.route("/lab1/error/403")
def error_403():
    return "доступ запрещён", 403

@app.route("/lab1/error/405")
def error_405():
    return "метод не разрешён", 405

@app.route("/lab1/error/418")
def error_418():
    return "я чайник", 418






@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
           <body> 
               <h1>web-сервер на flask</h1> 
               <a href="/lab1/author">author</a>
           </body> 
        </html>""", 200, {
             'X-Server': 'sample',
             'Content-Type': 'text/html; charset=utf-8'
             } 

@app.route("/lab1/author")
def author():
        name = "Gundareva Angela"
        group ="FBI-31"
        faculty = "FB"
        return """<!doctype html>
            <html>
                <body>
                    <p> Студент: """ + name + """</p>
                    <p> Группа: """ + group + """</p>
                    <p> Факультет: """ + faculty + """</p>
                    <a href="/lab1/web">web</a>
                </body>
            </html>""" 

@app.route('/lab1/image')
def image():
      path = url_for("static", filename="cat.jpg")
      css_path = url_for("static", filename="lab1.css")
      return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
       <h1>Кот</h1>
       <img src="''' + path + '''">
    </body>
</html>''', 200, {
        'Content-Language': 'ru',
        'X-Author': 'Gundareva A.A.',    
        'X-Framework': 'Flask'}


count = 0
@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time =datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
       Сколько раз вы сюда заходили: ''' + str(count) +'''
       <hr>
       Дата и время: ''' + str(time) + '''<br>
       Запрошенный адрес: ''' + str(url) + '''<br>
       Ваш IP-адрес: ''' + str(client_ip) + '''<br> 
       <hr>
       <a href="/lab1/reset_counter">Очистить счетчик</a>
    </body>
</html>
'''

@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
       Счетчик очищен!
       <hr>
       <a href="/lab1/counter">Вернуться к счетчику</a>
    </body>
</html>
'''

@app.route("/lab1/info")
def info():
      return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
       <h1> Создано успешно </h1>
       <div><i>что-то создано...</i></div>
    </body>
</html>
''', 201



@app.route("/lab1/cause_error")
def cause_error():
    
    x = 1 / 0
    return str(x)


@app.errorhandler(500)
def internal_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Ошибка сервера</title>
        <style>
            body {
                text-align: center;
                background: linear-gradient(135deg, #ffd6e7 0%, #ffc2d6 50%, #ffafc5 100%);
                color: #d63384;
                margin: 0;
                padding: 50px;
                font-family: 'Arial', sans-serif;
            }
        </style>
    </head>
    <body>
        <h1>Внутренняя ошибка сервера (500)</h1>
        <p>Произошла непредвиденная ошибка на сервере</p>
    </body>
</html>
''', 500



@app.route('/lab2/a')
def a():
    return 'без слеша'

@app.route('/lab2/a/')
def a2():
    return 'со слешем'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "Цветок  " + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p> Название нового цветка: {name} </p>
    <p> Всего цветов: {len(flower_list)}</p>
    <p> Полный список: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
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