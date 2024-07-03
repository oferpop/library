from flask import Blueprint, jsonify, request
from database import db
from models.loan import Loan
from models.book import Book
from datetime import datetime, timedelta
from flask import make_response
bp = Blueprint('loans', __name__)




@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response
@bp.route('/loans', methods=['GET'])
def get_loans():
    loans = Loan.query.all()
    return jsonify([{'id': l.id, 'cust_id': l.cust_id, 'book_id': l.book_id, 'loan_date': l.loan_date.isoformat(), 'return_date': l.return_date.isoformat() if l.return_date else None} for l in loans])

@bp.route('/loans', methods=['POST'])
def loan_book():
    data = request.json
    book = Book.query.get(data['book_id'])
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    
    max_days = {1: 10, 2: 5, 3: 2}
    return_date = datetime.utcnow() + timedelta(days=max_days[book.type])
    
    new_loan = Loan(cust_id=data['cust_id'], book_id=data['book_id'], loan_date=datetime.utcnow(), return_date=return_date)
    db.session.add(new_loan)
    db.session.commit()
    return jsonify({'message': 'Book loaned successfully'}), 201

@bp.route('/loans/return', methods=['POST'])
def return_book():
    data = request.json
    loan = Loan.query.filter_by(book_id=data['book_id'], return_date=None).first()
    if not loan:
        return jsonify({'message': 'Loan not found'}), 404
    
    loan.return_date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Book returned successfully'}), 200

@bp.route('/loans/late', methods=['GET'])
def get_late_loans():
    today = datetime.utcnow()
    late_loans = Loan.query.filter(Loan.return_date < today, Loan.return_date == None).all()
    return jsonify([{'id': l.id, 'cust_id': l.cust_id, 'book_id': l.book_id, 'loan_date': l.loan_date.isoformat(), 'return_date': l.return_date.isoformat() if l.return_date else None} for l in late_loans])