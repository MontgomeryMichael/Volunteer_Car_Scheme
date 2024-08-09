""" Module contains routes for the trip service. """

from datetime import datetime
from flask import request, jsonify, Blueprint
from models import db, TripRequest, ConfirmedTrip

routes = Blueprint('routes', __name__)

@routes.route('/trips/requests', methods=['POST'])
def create_trip_request():
    """ Method to create a trip request."""
    try:
        data = request.get_json()
        if 'date' in data:
            data['date'] = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            data['time'] = datetime.strptime(data['time'], '%H:%M').time()
        new_trip_request = TripRequest(**data)
        db.session.add(new_trip_request)
        db.session.commit()
        return jsonify({'message': 'Trip request created successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/requests/<int:trip_request_id>/confirm', methods=['PUT'])
def confirm_trip(trip_request_id):
    """ Method to confirm a trip request."""
    try:
        data = request.get_json()
        if 'confirmation_date' in data:
            data['confirmation_date'] = datetime.strptime(data['confirmation_date'], '%Y-%m-%d').date()
        if 'confirmation_time' in data:
            data['confirmation_time'] = datetime.strptime(data['confirmation_time'], '%H:%M').time()
        trip_request = TripRequest.query.get(trip_request_id)
        customer_id = trip_request.customer_id
        new_confirmed_trip = ConfirmedTrip(trip_request_id=trip_request_id,
                                           customer_id=customer_id,**data)
        trip_request.status = 'Confirmed'
        db.session.add(new_confirmed_trip)
        db.session.commit()
        return jsonify({'message': 'Trip confirmed successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400
    
@routes.route('/trips/requests/pending', methods=['GET'])
def get_pending_trip_requests():
    """ Method to get all pending trip requests."""
    try:
        trip_requests = TripRequest.query.filter_by(status='Pending').all()
        return jsonify([trip_request.to_dict() for trip_request in trip_requests]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/requests/declined', methods=['GET'])
def get_declined_trip_requests():
    """ Method to get all declined trip requests."""
    try:
        trip_requests = TripRequest.query.filter_by(status='Declined').all()
        return jsonify([trip_request.to_dict() for trip_request in trip_requests]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/requests', methods=['GET'])
def get_trip_requests():
    """ Method to get all trip requests."""
    try:
        trip_requests = TripRequest.query.all()
        return jsonify([trip_request.to_dict() for trip_request in trip_requests]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/requests/<int:trip_request_id>', methods=['GET'])
def get_trip_request(trip_request_id):
    """ Method to get a trip request by id."""
    try:
        trip_request = TripRequest.query.get(trip_request_id)
        return jsonify(trip_request.to_dict()), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/confirmed', methods=['GET'])
def get_confirmed_trips():
    """ Method to get all confirmed trips."""
    try:
        confirmed_trips = ConfirmedTrip.query.all()
        return jsonify([confirmed_trip.to_dict() for confirmed_trip in confirmed_trips]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/confirmed/driver/<int:driver_id>', methods=['GET'])
def get_confirmed_trip_by_driver(driver_id):
    """ Method to get a confirmed trip by driver_id."""
    try:
        confirmed_trips = ConfirmedTrip.query.filter_by(driver_id=driver_id).all()
        return jsonify([confirmed_trip.to_dict() for confirmed_trip in confirmed_trips]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/confirmed/customer/<int:customer_id>', methods=['GET'])
def get_confirmed_trip_by_customer(customer_id):
    """ Method to get a confirmed trip by customer_id."""
    try:
        confirmed_trips = ConfirmedTrip.query.filter_by(customer_id=customer_id).all()
        return jsonify([confirmed_trip.to_dict() for confirmed_trip in confirmed_trips]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/requests/<int:trip_request_id>/decline', methods=['PUT'])
def decline_trip(trip_request_id):
    """ Method to decline a trip request."""
    try:
        trip_request = TripRequest.query.get(trip_request_id)
        trip_request.status = 'Declined'
        db.session.commit()
        return jsonify({'message': 'Trip declined successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/requests/<int:trip_request_id>', methods=['DELETE'])
def delete_trip_request(trip_request_id):
    """ Method to delete a trip request."""
    try:
        trip_request = TripRequest.query.get(trip_request_id)
        db.session.delete(trip_request)
        db.session.commit()
        return jsonify({'message': 'Trip request deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@routes.route('/trips/confirmed/<int:confirmed_trip_id>', methods=['DELETE'])
def delete_confirmed_trip(confirmed_trip_id):
    """ Method to delete a confirmed trip."""
    try:
        confirmed_trip = ConfirmedTrip.query.get(confirmed_trip_id)
        trip_request = TripRequest.query.get(confirmed_trip.trip_request_id)
        trip_request.status = 'Declined'
        db.session.delete(confirmed_trip)
        db.session.commit()
        return jsonify({'message': 'Trip deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400