from flask import Blueprint, url_for, request, redirect, abort
import datetime
lab1 = Blueprint('lab1' ,__name__)


@lab1.route("/lab1")
def lab():
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


@lab1.route("/lab1/error/400")
def error_400():
    return "неверный запрос", 400


@lab1.route("/lab1/error/401")
def error_401():
    return "требуется авторизация", 401


@lab1.route("/lab1/error/402")
def error_402():
    return "требуется оплата", 402


@lab1.route("/lab1/error/403")
def error_403():
    return "доступ запрещён", 403


@lab1.route("/lab1/error/405")
def error_405():
    return "метод не разрешён", 405


@lab1.route("/lab1/error/418")
def error_418():
    return "я чайник", 418


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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


@lab1.route('/lab1/image')
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
@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/reset_counter')
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


@lab1.route("/lab1/info")
def info():
      return redirect("/lab1/author")


@lab1.route("/lab1/created")
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


@lab1.route("/lab1/cause_error")
def cause_error():
    
    x = 1 / 0
    return str(x)


