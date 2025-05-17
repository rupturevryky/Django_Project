import pytest
from datetime import datetime

def test_base_template_footer(client):
    response = client.get("/")
    assert 'Мишин Владислав Анатольевич' in response.text
    assert '231-352' in response.text

def test_post_route_exists(client):
    response = client.get("/posts/0")
    assert response.status_code == 200

def test_post_template_rendering(client, mocker):
    mock_posts = [{
        'title': 'Test Title',
        'author': 'Test Author',
        'date': datetime(2023, 1, 1),
        'text': 'Test Content',
        'image_id': 'test.jpg',
        'comments': []
    }]
    mocker.patch("app.posts_list", return_value=mock_posts)
    
    response = client.get("/posts/0")
    assert 'Test Title' in response.text
    assert 'Test Author' in response.text
    assert '01.01.2023' in response.text

def test_post_404(client):
    response = client.get("/posts/999")
    assert response.status_code == 404

def test_comment_form_presence(client):
    response = client.get("/posts/0")
    assert 'Оставьте комментарий' in response.text
    assert '<form method="POST"' in response.text

def test_comments_rendering(client, mocker):
    mock_posts = [{
        'title': 'Test Post',
        'author': 'Test Author',
        'date': datetime(2023, 1, 1),
        'text': 'Test Content',
        'image_id': 'test.jpg',
        'comments': [
            {'author': 'User1', 'text': 'Comment1', 'replies': [], 'date': datetime(2023, 1, 1)},
            {'author': 'User2', 'text': 'Comment2', 'replies': [
                {'author': 'User3', 'text': 'Reply1', 'date': datetime(2023, 1, 1)}
            ], 'date': datetime(2023, 1, 1)}
        ]
    }]
    mocker.patch("app.posts_list", return_value=mock_posts)
    
    response = client.get("/posts/0")
    assert 'User1' in response.text
    assert 'Comment1' in response.text
    assert 'Reply1' in response.text

def test_image_rendering(client, mocker):
    mock_posts = [{
        'title': 'Test Post',
        'author': 'Test Author',
        'date': datetime(2023, 1, 1),
        'text': 'Test Content',
        'image_id': 'test.jpg',
        'comments': []
    }]
    mocker.patch("app.posts_list", return_value=mock_posts)
    
    response = client.get("/posts/0")
    assert 'src="/static/images/test.jpg"' in response.text

def test_post_content_presence(client, mocker):
    mock_posts = [{
        'title': 'Test Post',
        'author': 'Test Author',
        'date': datetime(2023, 1, 1),
        'text': 'Sample post content',
        'image_id': 'test.jpg',
        'comments': []
    }]
    mocker.patch("app.posts_list", return_value=mock_posts)
    
    response = client.get("/posts/0")
    assert 'Sample post content' in response.text

def test_post_date_format(client, mocker):
    mock_posts = [{
        'title': 'Test Post',
        'author': 'Test Author',
        'date': datetime(2023, 12, 31, 15, 30),
        'text': 'Test Content',
        'image_id': 'test.jpg',
        'comments': []
    }]
    mocker.patch("app.posts_list", return_value=mock_posts)
    
    response = client.get("/posts/0")
    assert '31.12.2023 в 15:30' in response.text

def test_post_404(client, mocker):
    mock_posts = [{
        'title': 'Test Post',
        'author': 'Test Author',
        'date': datetime(2023, 1, 1),
        'text': 'Test Content',
        'image_id': 'test.jpg',
        'comments': []
    }]
    mocker.patch("app.posts_list", return_value=mock_posts)
    
    response = client.get("/posts/999")
    assert response.status_code == 404

# Добавьте еще 6 тестов по аналогии, проверяя:
# - Разные сценарии комментариев
# - Граничные случаи с датами
# - Особые случаи форматирования
# - Наличие всех элементов интерфейса