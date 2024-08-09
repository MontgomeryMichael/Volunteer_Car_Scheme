"""Module contains routes for the driver service."""

from flask import request, jsonify, Blueprint
from models import db, Driver

routes = Blueprint('routes', __name__)

@routes.route('/drivers', methods=['POST'])
def create_driver():
    """Method to create a new driver.  """
    try:
        data = request.get_json()
        new_driver = Driver(**data)
        db.session.add(new_driver)
        db.session.commit()
        return jsonify({'message': 'Driver profile created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/drivers/<int:driver_id>', methods=['GET'])
def get_driver(driver_id):
    """Method returns driver details using driver_id."""
    try:
        driver = Driver.query.get(driver_id)
        if driver:
            return jsonify(driver.to_dict()), 200
        else:
            return jsonify({"error": "Driver not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/drivers/details/<string:username>', methods=['GET'])
def get_driver_username(username):
    """Method returns driver details using username."""
    try:
        driver = Driver.query.filter_by(username=username).first()
        if driver:
            return jsonify(driver.to_dict()), 200
        else:
            return jsonify({"error": "Driver not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/drivers/<string:username>', methods=['GET'])
def get_driver_by_username(username):
    """Method returns driver_id using username."""
    try:
        driver = Driver.query.filter_by(username=username).first()
        if driver:
            return jsonify({'driver_id': driver.driver_id}), 200
        else:
            return jsonify({"error": "Driver not found"}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/drivers/all', methods=['GET'])
def get_all_drivers():
    """Method returns all drivers."""
    try:
        drivers = Driver.query.all()
        drivers = [driver.to_dict() for driver in drivers]
        return jsonify(drivers), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    

@routes.route('/drivers/<int:driver_id>', methods=['PUT'])
def update_driver(driver_id):
    """Method to update driver profile."""
    try:
        data = request.get_json()
        driver = Driver.query.get(driver_id)
        if not driver:
            return jsonify({"error": "Driver not found"}), 404
        for key, value in data.items():
            setattr(driver, key, value)
        db.session.commit()
        return jsonify({'message': 'Driver profile updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/drivers/<int:driver_id>', methods=['DELETE'])
def delete_driver(driver_id):
    """Method to delete driver profile."""
    try:
        driver = Driver.query.get(driver_id)
        if not driver:
            return jsonify({"error": "Driver not found"}), 404
        db.session.delete(driver)
        db.session.commit()
        return jsonify({'message': 'Driver profile deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
