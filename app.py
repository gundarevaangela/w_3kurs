from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

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
       <a href="/web">Вернуться на главную</a>
    </body>
</html>
''', 404

@app.route("/web")
def web():
    return """<!doctype html> 
        <html> 
           <body> 
               <h1>web-сервер на flask</h1> 
               <a href="/author">author</a>
           </body> 
        </html>""", 200, {
             'X-Server': 'sample',
             'Content-Type': 'text/html; charset=utf-8'
             } 

@app.route("/author")
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
                    <a href="/web">web</a>
                </body>
            </html>""" 
@app.route('/image')
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
</html>
'''

count = 0
@app.route('/counter')
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
    </body>
</html>
'''

@app.route("/info")
def info():
      return redirect("/author")

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