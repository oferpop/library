from flask import Blueprint, jsonify, request
from database import db
from models.book import Book
from flask import make_response

bp = Blueprint('books', __name__)


@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
@bp.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': b.id, 'name': b.name, 'author': b.author, 'year_published': b.year_published, 'type': b.type} for b in books])

@bp.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = Book(name=data['name'], author=data['author'], year_published=data['year_published'], type=data['type'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@bp.route('/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book removed successfully'}), 200

@bp.route('/books/search', methods=['GET'])
def find_book():
    name = request.args.get('name')
    books = Book.query.filter(Book.name.ilike(f'%{name}%')).all()
    return jsonify([{'id': b.id, 'name': b.name, 'author': b.author, 'year_published': b.year_published, 'type': b.type} for b in books])

    