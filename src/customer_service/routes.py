""" Module contains routes for customer service. """

from flask import request, jsonify, Blueprint
from models import Customer, db

routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def create_customer():
    """Method to create a customer profile."""
    try:
        data = request.get_json()
        new_customer = Customer(**data)
        db.session.add(new_customer)
        db.session.commit()
        return jsonify({'message': 'Customer profile created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Method returns customer profile using their ID."""
    try:
        customer = Customer.query.get(customer_id)
        if customer:
            return jsonify(customer.to_dict()), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/customers/<string:username>', methods=['GET'])
def get_customer_by_username(username):
    """Method returns customer ID using their username."""
    try:
        customer = Customer.query.filter_by(username=username).first()
        if customer:
            return jsonify({'customer_id': customer.customer_id}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/customers/details/<string:username>', methods=['GET'])
def get_customer_details(username):
    """Method returns customer profile using their username."""
    try:
        customer = Customer.query.filter_by(username=username).first()
        if customer:
            return jsonify(customer.to_dict()), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/customers/all', methods=['GET'])
def get_all_customers():
    """Method returns all customer profiles."""
    try:
        customers = Customer.query.all()
        customers = [customer.to_dict() for customer in customers]
        return jsonify(customers), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    """Method updates a customer profile."""
    try:
        data = request.get_json()
        customer = Customer.query.get(customer_id)
        if customer:
            for key, value in data.items():
                setattr(customer, key, value)
            db.session.commit()
            return jsonify({'message': 'Customer profile updated successfully!'}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    """Method deletes a customer profile."""
    try:
        customer = Customer.query.get(customer_id)
        if customer:
            db.session.delete(customer)
            db.session.commit()
            return jsonify({'message': 'Customer profile deleted successfully!'}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400
