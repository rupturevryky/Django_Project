import re
import random
from functools import lru_cache
from faker import Faker
import os
from flask import Flask, render_template, request, make_response, redirect, url_for, abort, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

fake = Faker()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Добавьте секретный ключ
application = app

# Настройка LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Загрузчик пользователя
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

images_ids = ['7d4e9175-95ea-4c5f-8be5-92a6b708bb3c',
              '2d2ab7df-cdbc-48a8-a936-35bba702def5',
              '6e12f3de-d5fd-4ebb-855b-8cbc485278b7',
              'afc2cfe7-5cac-4b80-9b9a-d5c65ef0c728',
              'cab5b7f2-774e-4884-a200-0c0180fa777f']

def generate_comments(replies=True):
    comments = []
    for _ in range(random.randint(1, 3)):
        comment = { 'author': fake.name(), 'text': fake.text() }
        if replies:
            comment['replies'] = generate_comments(replies=False)
        comments.append(comment)
    return comments

def generate_post(i):
    return {
        'title': 'Заголовок поста',
        'text': fake.paragraph(nb_sentences=100),
        'author': fake.name(),
        'date': fake.date_time_between(start_date='-2y', end_date='now'),
        'image_id': f'{images_ids[i]}.jpg',
        'comments': generate_comments()
    }

@lru_cache
def posts_list():
    return sorted([generate_post(i) for i in range(5)], key=lambda p: p['date'], reverse=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/posts')
def posts():
    return render_template('posts.html', title='Посты', posts=posts_list())

@app.route('/posts/<int:index>')
def post(index):
    posts = posts_list()
    if index < 0 or index >= len(posts):
        abort(404)
    p = posts[index]
    return render_template('post.html', title=p['title'], post=p)

@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/url_params')
def url_params():
    return render_template('url_params.html', params=request.args)

@app.route('/headers')
def headers():
    return render_template('headers.html', headers=request.headers)

@app.route('/cookies')
def cookies():
    cookie_value = request.cookies.get('lab2_cookie')
    response = make_response(render_template('cookies.html', cookie_value=cookie_value))
    
    if not cookie_value:
        response.set_cookie('lab2_cookie', 'Hello_from_Lab2!', max_age=60*5)
    else:
        response.delete_cookie('lab2_cookie')

    return response

@app.route('/form_params', methods=['GET', 'POST'])
def form_params():
    data = {}
    if request.method == 'POST':
        data = dict(request.form)
    return render_template('form_params.html', data=data)

@app.route('/phone', methods=['GET', 'POST'])
def phone():
    error = None
    formatted = None
    phone_value = request.form.get('phone', '') if request.method == 'POST' else ''

    if request.method == 'POST' and phone_value.strip():
        # Удаляем все нецифровые символы кроме +
        cleaned = re.sub(r'[^\d+]', '', phone_value)
        digits = re.sub(r'\D', '', phone_value)  # Только цифры
        
        # Проверка допустимых символов
        if not re.match(r'^[\d+\-(). ]+$', phone_value):
            error = 'Недопустимый ввод. В номере встречаются недопустимые символы.'
        else:
            # Проверка длины
            if digits.startswith(('7', '8')):
                required_length = 11
            else:
                required_length = 10
                
            if len(digits) != required_length:
                error = 'Недопустимый ввод. Неверное количество цифр.'
            else:
                # Форматирование
                last_10 = digits[-10:]
                formatted = f'8-{last_10[0:3]}-{last_10[3:6]}-{last_10[6:8]}-{last_10[8:10]}'

    return render_template('phone.html',
                         error=error,
                         phone=phone_value,
                         formatted=formatted)


# Лабораторная работа №3
@app.route('/visits')
def visits():
    # Счетчик посещений
    session['visits_count'] = session.get('visits_count', 0) + 1
    return render_template('visits.html', visits=session['visits_count'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if username == 'user' and password == 'qwerty':
            user = User(username)
            login_user(user, remember=remember)
            flash('Successful login', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Incorrect username or password', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out of the system', 'info')
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')


# if __name__ == '__main__':
#     app.run()
