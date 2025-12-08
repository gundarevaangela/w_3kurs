import os
from flask import Blueprint, render_template, request, abort, current_app
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='angela_gundareva',
            user='angela_gundareva',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


def validate_film(film):
    
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
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
            rows = cur.fetchall()
            films = []
            for r in rows:
                films.append({
                    'id': r['id'],
                    'title': r.get('title') or '',
                    'title_ru': r.get('title_ru') or '',
                    'year': r.get('year'),
                    'description': r.get('description') or ''
                })
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films ORDER BY id;")
            rows = cur.fetchall()
            films = []
            for r in rows:
                films.append({
                    'id': r['id'],
                    'title': r['title'] or '',
                    'title_ru': r['title_ru'] or '',
                    'year': r['year'],
                    'description': r['description'] or ''
                })
    finally:
        db_close(conn, cur)
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = %s;", (id,))
            row = cur.fetchone()
            if not row:
                db_close(conn, cur)
                abort(404)
            film = {
                'id': row['id'],
                'title': row.get('title') or '',
                'title_ru': row.get('title_ru') or '',
                'year': row.get('year'),
                'description': row.get('description') or ''
            }
        else:
            cur.execute("SELECT id, title, title_ru, year, description FROM films WHERE id = ?;", (id,))
            row = cur.fetchone()
            if not row:
                db_close(conn, cur)
                abort(404)
            film = {
                'id': row['id'],
                'title': row['title'] or '',
                'title_ru': row['title_ru'] or '',
                'year': row['year'],
                'description': row['description'] or ''
            }
    finally:
        db_close(conn, cur)
    return film

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
            if not cur.fetchone():
                db_close(conn, cur)
                abort(404)
            cur.execute("DELETE FROM films WHERE id = %s;", (id,))
        else:
            cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
            if not cur.fetchone():
                db_close(conn, cur)
                abort(404)
            cur.execute("DELETE FROM films WHERE id = ?;", (id,))
    finally:
        db_close(conn, cur)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM films WHERE id = %s;", (id,))
            if not cur.fetchone():
                db_close(conn, cur)
                abort(404)
        else:
            cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
            if not cur.fetchone():
                db_close(conn, cur)
                abort(404)
    finally:
        db_close(conn, cur)
    
    film = request.get_json()
    if film is None:
        return {'error': 'Invalid JSON'}, 400
    
    # Валидация всех полей
    errors = validate_film(film)
    if errors:
        return errors, 400
    
    conn, cur = db_connect()
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s;
            """, (film.get('title'), film.get('title_ru'), film.get('year'), film.get('description'), id))
        else:
            cur.execute("""
                UPDATE films SET title = ?, title_ru = ?, year = ?, description = ? WHERE id = ?;
            """, (film.get('title'), film.get('title_ru'), film.get('year'), film.get('description'), id))
    finally:
        db_close(conn, cur)

    #  обновлённый фильм
    return get_film(id) 

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film is None:
        return {'error': 'Invalid JSON'}, 400
    
    # Валидация всех полей
    errors = validate_film(film)
    if errors:
        return errors, 400
    
    conn, cur = db_connect()
    new_id = None
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description)
                VALUES (%s, %s, %s, %s) RETURNING id;
            """, (film.get('title'), film.get('title_ru'), film.get('year'), film.get('description')))
            row = cur.fetchone()
            new_id = row['id'] if row else None
        else:
            cur.execute("""
                INSERT INTO films (title, title_ru, year, description)
                VALUES (?, ?, ?, ?);
            """, (film.get('title'), film.get('title_ru'), film.get('year'), film.get('description')))
            new_id = cur.lastrowid
    finally:
        db_close(conn, cur)

    if new_id is None:
        return {'error': 'Insert failed'}, 500
    return str(new_id), 201