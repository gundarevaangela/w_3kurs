from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)



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
    </body>
</html>
'''

def get_navigation_links():
    return '''
    <hr>
    <h3>Навигация:</h3>
    <a href="/lab1/web">Главная</a> |
    <a href="/lab1/author">Автор</a> |
    <a href="/lab1/image">Изображение</a> |
    <a href="/lab1/counter">Счетчик</a> |
    <a href="/lab1/info">Инфо</a> |
   
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




@app.errorhandler(404)
def not_found(err):
    osh = url_for("static", filename="404.jpeg") 
    return '''
<!doctype html>
<html>
    <body>
       <h1>Ошибка 404 - Страница не найдена</h1>
       <p>К сожалению, такой страницы не существует</p>
       <img src="''' + osh + '''">
       <br>
       <a href="/lab1/web">Вернуться на главную</a>
       
    </body>
</html>
''', 404

@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
           <body> 
               <h1>web-сервер на flask</h1> 
               <a href="/lab1/author">author</a>
               """ + get_navigation_links() + """
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
                    """ + get_navigation_links() + """
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
       ''' + get_navigation_links() + '''
    </body>
</html>
'''

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
       ''' + get_navigation_links() + '''
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
       ''' + get_navigation_links() + '''
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