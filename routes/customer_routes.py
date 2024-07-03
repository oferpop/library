from flask import Blueprint, jsonify, request
from database import db
from models.customer import Customer
from flask import make_response
bp = Blueprint('customers', __name__)


@bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

@bp.route('/customers', methods=['GET'])
def get_customers():
    customers = Customer.query.all()
    return jsonify([{'id': c.id, 'name': c.name, 'city': c.city, 'age': c.age} for c in customers])

@bp.route('/customers', methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(name=data['name'], city=data['city'], age=data['age'])
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

@bp.route('/customers/<int:id>', methods=['DELETE'])
def remove_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer removed successfully'}), 200

@bp.route('/customers/search', methods=['GET'])
def find_customer():
    name = request.args.get('name')
    customers = Customer.query.filter(Customer.name.ilike(f'%{name}%')).all()
    return jsonify([{'id': c.id, 'name': c.name, 'city': c.city, 'age': c.age} for c in customers])