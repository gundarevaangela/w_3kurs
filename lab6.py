from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

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

@lab6.route("/lab6/")
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute('SELECT * FROM offices ORDER BY number')
            else:
                cur.execute('SELECT * FROM offices ORDER BY number')
                
            offices = cur.fetchall()
            
            # Конвертируем в обычный список словарей для JSON
            offices_list = []
            for office in offices:
                if current_app.config['DB_TYPE'] == 'postgres':
                    offices_list.append(dict(office))
                else:
                    offices_list.append({
                        'number': office['number'],
                        'tenant': office['tenant'],
                        'price': office['price']
                    })
            
            return {
                'jsonrpc': '2.0',
                'result': offices_list,
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }
    
    elif data['method'] == 'booking':
        office_number = data['params']
        
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute('SELECT tenant FROM offices WHERE number = %s', (office_number,))
            else:
                cur.execute('SELECT tenant FROM offices WHERE number = ?', (office_number,))
                
            office = cur.fetchone()
            
            if office['tenant']:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id 
                }
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', (login, office_number))
            else:
                cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', (login, office_number))
                
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    elif data['method'] == 'cancellation':
        office_number = data['params']
        
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute('SELECT tenant FROM offices WHERE number = %s', (office_number,))
            else:
                cur.execute('SELECT tenant FROM offices WHERE number = ?', (office_number,))
                
            office = cur.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            if not office['tenant']:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'Office is not booked'
                    },
                    'id': id
                }
            
            if office['tenant'] != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'You can only cancel your own booking'
                    },
                    'id': id
                }
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute('UPDATE offices SET tenant = %s WHERE number = %s', ('', office_number))
            else:
                cur.execute('UPDATE offices SET tenant = ? WHERE number = ?', ('', office_number))
                
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }