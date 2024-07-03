# backend/tests/test_book.py
import pytest
from app import app, db
from models.book import Book

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_add_book(client):
    response = client.post('/books', json={
        'name': 'Test Book',
        'author': 'Test Author',
        'year_published': 2021,
        'type': 1
    })
    assert response.status_code == 201
    assert b'Book added successfully' in response.data

# Add more tests for other book operations

# Similarly, create test_customer.py and test_loan.py with appropriate tests