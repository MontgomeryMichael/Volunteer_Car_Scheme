"""Module for routes in the coordinator service."""

from flask import Blueprint, request, jsonify
from models import db, Coordinator, PendingDriverRegistration, PendingCustomerRegistration
import requests

coordinator_routes = Blueprint('coordinator_routes', __name__)

@coordinator_routes.route('/coordinators/pending-customer-registrations', methods=['POST'])
def add_pending_customer_registration():
    """Method to add a pending customer registration."""
    try:
        data = request.get_json()
        new_registration = PendingCustomerRegistration(**data)
        db.session.add(new_registration)
        db.session.commit()
        return jsonify({'message': 'Customer registration added successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-customer-registrations', methods=['GET'])
def view_pending_customer_registrations():
    """Method to view all pending customer registrations."""
    try:
        registrations = PendingCustomerRegistration.query.filter_by(status='Pending').all()
        registrations = [registration.to_dict() for registration in registrations]
        return jsonify(registrations), 200                                                               
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/approved-customer-registrations', methods=['GET'])
def view_approved_customer_registrations():
    """Method to view all the approved customer registrations."""
    try:
        registrations = PendingCustomerRegistration.query.filter_by(status='Approved').all()
        registrations = [registration.to_dict() for registration in registrations]
        return jsonify(registrations), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/rejected-customer-registrations', methods=['GET'])
def view_rejected_customer_registrations():
    """Method to view all the rejected customer registrations."""
    try: 
        registrations = PendingCustomerRegistration.query.filter_by(status='Rejected').all()
        registrations = [registration.to_dict() for registration in registrations]
        return jsonify(registrations), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-customer-registrations/<int:registration_id>', methods=['GET'])
def view_specific_customer_registration(registration_id):
    """Method to view a specific pending customer registration."""
    try:
        registration = PendingCustomerRegistration.query.get_or_404(registration_id)
        return jsonify(registration.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-customer-registrations/<int:registration_id>/reject', methods=['PUT'])
def reject_customer_registration(registration_id):
    """Method to reject a specific pending customer registration."""
    try:
        registration = PendingCustomerRegistration.query.get_or_404(registration_id)
        registration.status = 'Rejected'
        db.session.commit()
        return jsonify({'message': 'Registration rejected successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-driver-registrations', methods=['POST'])
def add_pending_driver_registration():
    """Method to add a pending driver registration."""
    try:
        data = request.get_json()
        new_registration = PendingDriverRegistration(**data)
        db.session.add(new_registration)
        db.session.commit()
        return jsonify({'message': 'Driver registration added successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-driver-registrations', methods=['GET'])
def view_pending_driver_registrations():
    """Method to view all pending driver registrations."""
    try:
        registrations = PendingDriverRegistration.query.filter_by(status='Pending').all()
        registrations = [registration.to_dict() for registration in registrations]
        return jsonify(registrations), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/approved-driver-registrations', methods=['GET'])
def view_approved_driver_registrations():
    """Method to view all the approved driver registrations."""
    try:
        registrations = PendingDriverRegistration.query.filter_by(status='Approved').all()
        registrations = [registration.to_dict() for registration in registrations]
        return jsonify(registrations), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/rejected-driver-registrations', methods=['GET'])
def view_rejected_driver_registrations():
    """Method to view all the rejected driver registrations."""
    try:
        registrations = PendingDriverRegistration.query.filter_by(status='Rejected').all()
        registrations = [registration.to_dict() for registration in registrations]
        return jsonify(registrations), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-driver-registrations/<int:registration_id>', methods=['GET'])
def view_specific_driver_registration(registration_id):
    """Method to view a specific pending driver registration."""
    try:
        registration = PendingDriverRegistration.query.get_or_404(registration_id)
        return jsonify(registration.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-customer-registrations/<int:registration_id>/approve', methods=['PUT'])
def approve_customer_registration(registration_id):
    """Method to approve a specific pending customer registration."""
    try:
        registration = PendingCustomerRegistration.query.get_or_404(registration_id)
        registration.status = 'Approved'
        db.session.commit()
        if registration.status == 'Approved':
            customer_data = {
                'username': registration.username,
                'first_name': registration.first_name,
                'last_name': registration.last_name,
                'address_line1': registration.address_line1,
                'address_line2': registration.address_line2,
                'town': registration.town,
                'county': registration.county,
                'postcode': registration.postcode,
                'mobile': registration.mobile,
                'email': registration.email
            }
            response = requests.post('http://customer_service:5002/register', json=customer_data)
            user_data = {
                'username': registration.username,
                'password': registration.password,
                'role': 'Customer'
            }
            response = requests.post('http://user_service:5001/register', json=user_data)
        return jsonify({'message': 'Registration approved successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-driver-registrations/<int:registration_id>/approve', methods=['PUT'])
def approve_driver_registration(registration_id):
    """Method to approve a specific pending driver"""
    try:
        registration = PendingDriverRegistration.query.get_or_404(registration_id)
        registration.status = 'Approved'
        db.session.commit()
        if registration.status == 'Approved':
            driver_data = {
                'username': registration.username,
                'first_name': registration.first_name,
                'last_name': registration.last_name,
                'license': registration.license,
                'car_make': registration.car_make,
                'car_model': registration.car_model,
                'car_reg': registration.car_reg,
                'car_colour': registration.car_colour,
                'email': registration.email,
                'mobile': registration.mobile
            }
            response = requests.post('http://driver_service:5003/drivers', json=driver_data)
            user_data = {
                'username': registration.username,
                'password': registration.password,
                'role': 'Driver'
            }
            response = requests.post('http://user_service:5001/register', json=user_data)
        return jsonify({'message': 'Registration approved successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@coordinator_routes.route('/coordinators/pending-driver-registrations/<int:registration_id>/reject', methods=['PUT'])
def reject_driver_registration(registration_id):
    """Method to reject a specific pending driver registration."""
    try:
        registration = PendingDriverRegistration.query.get_or_404(registration_id)
        registration.status = 'Rejected'
        db.session.commit()
        return jsonify({'message': 'Registration rejected successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
