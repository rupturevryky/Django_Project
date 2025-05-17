from datetime import datetime
import pytest
from flask import template_rendered
from contextlib import contextmanager
from app import app as application

@pytest.fixture
def app():
    return application

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

@pytest.fixture
def posts_list():
    return [
        {
            'title': 'Test Post',
            'author': 'Test Author',
            'date': datetime(2023, 1, 1),
            'text': 'Test Content',
            'image_id': 'test.jpg',
            'comments': [
                {
                    'author': 'Commenter1', 
                    'text': 'Test Comment',
                    'replies': [
                        {'author': 'Replier1', 'text': 'Test Reply'}
                    ],
                    'date': datetime(2023, 1, 1)
                }
            ]
        }
    ]