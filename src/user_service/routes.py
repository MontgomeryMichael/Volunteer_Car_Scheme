""" Module contains routes for the user service. """

from flask import request, jsonify, Blueprint
from models import db, User
from sqlalchemy.exc import IntegrityError

routes = Blueprint('routes', __name__)

@routes.route('/register', methods=['POST'])
def register():
    """ Method to register a new user."""
    data = request.get_json()
    new_user = User(username=data['username'], password=data['password'], role=data['role'])
    if new_user.role not in ['Customer', 'Driver', 'customer', 'driver']:
        return jsonify({'message': 'Invalid role for registration'}), 400
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User already exists!'}), 409

@routes.route('/login', methods=['POST'])
def login():
    """ Method to login."""
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        return jsonify({'message': 'Login successful!',
                        'user_id': user.user_id, 'username': user.username, 'role': user.role}), 200
    return jsonify({'message': 'Invalid credentials!'}), 401

@routes.route('/users/<int:user_id>/roles', methods=['PUT'])
def update_role(user_id):
    """ Method to update a user role."""
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.role = data['role']
    db.session.commit()
    return jsonify({'message': 'User role updated successfully!'}), 200