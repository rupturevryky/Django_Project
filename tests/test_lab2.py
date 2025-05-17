import pytest

def test_url_params(client):
    response = client.get('/url_params?test=123&name=John')
    assert b'test' in response.data
    assert b'123' in response.data
    assert b'name' in response.data
    assert b'John' in response.data

def test_headers(client):
    response = client.get('/headers', headers={'Accept': 'text/html'})
    assert b'User-Agent' in response.data
    assert b'Accept' in response.data
    assert b'Host' in response.data

def test_cookies_set(client):
    response = client.get('/cookies')
    assert b'lab2_cookie=Hello_from_Lab2!' in response.headers.get('Set-Cookie', '').encode('utf-8')

def test_cookies_delete(client):
    client.set_cookie('lab2_cookie', 'test')  # Исправлено количество аргументов
    response = client.get('/cookies')
    assert 'lab2_cookie=;' in response.headers.get('Set-Cookie', '')

def test_cookies_flow(client):
    # Первый запрос - устанавливаем cookie
    response = client.get('/cookies')
    assert 'lab2_cookie=Hello_from_Lab2!' in response.headers.get('Set-Cookie', '')
    
    # Второй запрос - удаляем cookie
    response = client.get('/cookies')
    assert 'lab2_cookie=;' in response.headers.get('Set-Cookie', '')

def test_phone_valid(client):
    tests = [
        ('+7 (999) 123-45-67', b'8-999-123-45-67'),
        ('89991234567', b'8-999-123-45-67'),
        ('1234567890', b'8-123-456-78-90')
    ]
    for phone, expected in tests:
        response = client.post('/phone', data={'phone': phone})
        assert response.status_code == 200
        assert expected in response.data

def test_phone_invalid_chars(client):
    response = client.post('/phone', data={'phone': '12a345_6789'})
    assert 'недопустимые символы'.encode('utf-8') in response.data
    assert b'is-invalid' in response.data

def test_phone_invalid_length(client):
    tests = [
        ('+7123', 'Неверное количество цифр'),
        ('812345678901', 'Неверное количество цифр'),
        ('123456789', 'Неверное количество цифр')
    ]
    for phone, error in tests:
        response = client.post('/phone', data={'phone': phone})
        assert error.encode('utf-8') in response.data

def test_phone_formatting(client):
    tests = [
        ('+7 (123) 456-75-90', b'8-123-456-75-90'),
        ('8(921)123-45-67', b'8-921-123-45-67'),
        ('123.456.75.90', b'8-123-456-75-90')
    ]
    for phone, formatted in tests:
        response = client.post('/phone', data={'phone': phone})
        assert formatted in response.data

def test_form_params(client):
    response = client.post('/form_params', data={
        'name': 'John',
        'email': 'test@example.com'
    })
    assert b'name' in response.data
    assert b'John' in response.data
    assert b'email' in response.data
    assert b'test@example.com' in response.data

# Добавьте дополнительные тесты
def test_phone_valid_with_spaces(client):
    response = client.post('/phone', data={'phone': '+7 999 123 45 67'})
    assert b'8-999-123-45-67' in response.data

def test_phone_empty_input(client):
    response = client.post('/phone', data={'phone': ''})
    assert b'is-invalid' not in response.data

def test_headers_content_type(client):
    response = client.get('/headers', headers={'Content-Type': 'text/html'})
    assert b'Content-Type' in response.data
    assert b'text/html' in response.data

def test_url_params_encoding(client):
    response = client.get('/url_params?city=Москва')
    assert 'Москва'.encode('utf-8') in response.data