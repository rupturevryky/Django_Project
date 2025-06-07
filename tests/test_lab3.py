import pytest
from flask import url_for, session
from flask_login import current_user

def test_visits_counter(client):
    # Первое посещение
    response = client.get('/visits')
    assert b'1 time' in response.data
    
    # Второе посещение
    response = client.get('/visits')
    assert b'2 times' in response.data

def test_login_success(client):
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    
    assert b'Successful login' in response.data
    assert b'Secret Page' in response.data

def test_login_failure(client):
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'wrong'
    })
    
    assert b'Incorrect username or password' in response.data
    assert b'Log in' in response.data

def test_secret_page_access(client):
    # Неавторизованный доступ
    response = client.get('/secret', follow_redirects=True)
    assert b'Authorisation' in response.data
    assert b'You must log in' in response.data
    
    # Авторизуемся
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    })
    
    # Авторизованный доступ
    response = client.get('/secret')
    assert b'Secret Page' in response.data

def test_redirect_after_login(client):
    # Пытаемся получить доступ к секретной странице
    response = client.get('/secret')
    assert response.status_code == 302
    
    # Авторизуемся
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'next': '/secret'
    }, follow_redirects=True)
    
    assert b'Secret Page' in response.data

def test_remember_me(client):
    # Логинимся с включенным "Запомнить меня"
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    }, follow_redirects=True)
    
    # Проверяем наличие remember токена
    assert 'remember_token' in client.get_cookie_names()

def test_logout(client):
    # Логинимся
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    })
    
    # Выходим
    response = client.get('/logout', follow_redirects=True)
    assert b'You have logged out of the system' in response.data
    assert b'Log in' in response.data

def test_navbar_links_authenticated(client):
    # Логинимся
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    })
    
    response = client.get('/')
    assert b'Secret Page' in response.data
    assert b'Log out' in response.data
    assert b'Log in' not in response.data

def test_navbar_links_anonymous(client):
    response = client.get('/')
    assert b'Secret Page' not in response.data
    assert b'Log out' not in response.data
    assert b'Log in' in response.data

def test_session_counter_per_user(client):
    # Первый пользователь
    with client.session_transaction() as sess:
        sess['visits_count'] = 5
    
    response = client.get('/visits')
    assert b'6 times' in response.data
    
    # Второй пользователь (новая сессия)
    client2 = app.test_client()
    response = client2.get('/visits')
    assert b'1 time' in response.data