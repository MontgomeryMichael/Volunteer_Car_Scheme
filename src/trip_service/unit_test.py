"""Unit tests for the trip_service module."""

import unittest
from datetime import datetime
from app import app, db
from models import TripRequest, ConfirmedTrip

class TripRequestsTestCase(unittest.TestCase):
    """Unit tests for the trip requests."""
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(TripRequest( customer_id=1,
                                   date=datetime.strptime('2021-01-01', '%Y-%m-%d').date(),
                                   time=datetime.strptime('10:00', '%H:%M').time(),
                                   destination='Destination 1', duration='1 hour',
                                   additional_passenger='None', purpose='Work'))
        db.session.add(TripRequest(customer_id=2,
                                   date=datetime.strptime('2021-01-02', '%Y-%m-%d').date(),
                                   time=datetime.strptime('11:00', '%H:%M').time(),
                                   destination='Destination 2',
                                   duration='2 hours',
                                   additional_passenger='None',
                                   purpose='Meeting'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_trip_request(self):
        """ Test for creating a trip request."""
        response = self.app.post('/trips/requests', json={
            'customer_id': 3,
            'date': '2021-01-03',
            'time': '12:00',
            'destination': 'Destination 3',
            'duration': '3 hours',
            'additional_passenger': 'None',
            'purpose': 'Interview'
        })
        self.assertEqual(response.status_code, 201)

    def test_confirm_trip(self):
        """ Test for confirming a trip request."""
        response = self.app.put('/trips/requests/1/confirm', json={
            'confirmation_date': '2021-01-01',
            'confirmation_time': '10:00',
            'driver_id': 1
        })
        self.assertEqual(response.status_code, 200)

    def test_get_pending_trip_requests(self):
        """ Test for getting all pending trip requests."""
        response = self.app.get('/trips/requests/pending')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_get_declined_trip_requests(self):
        """ Test for getting all declined trip requests."""
        response = self.app.get('/trips/requests/declined')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    def test_get_trip_requests(self):
        """ Test for getting all trip requests.  """
        response = self.app.get('/trips/requests')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_delete_trip_request(self):
        """ Test for deleting a trip request. """
        response = self.app.delete('/trips/requests/1')
        self.assertEqual(response.status_code, 200)

class ConfirmedTripsTestCase(unittest.TestCase):
    """Unit tests for confirmed trips."""
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(TripRequest(customer_id=1,
                                   date=datetime.strptime('2021-01-01', '%Y-%m-%d').date(),
                                   time=datetime.strptime('10:00', '%H:%M').time(),
                                   destination='Destination 1', duration='1 hour',
                                   additional_passenger='None', purpose='Work', status='Confirmed'))
        db.session.add(TripRequest(customer_id=2,
                                      date=datetime.strptime('2021-01-02', '%Y-%m-%d').date(),
                                      time=datetime.strptime('11:00', '%H:%M').time(),
                                      destination='Destination 2',
                                      duration='2 hours',
                                      additional_passenger='None',
                                      purpose='Meeting', status='Confirmed'))
        db.session.commit()
        db.session.add(ConfirmedTrip(trip_request_id=1, customer_id=1,
                                    driver_id=1,
                                    confirmation_date=datetime.strptime('2021-01-01','%Y-%m-%d').date(),
                                    confirmation_time=datetime.strptime('10:00', '%H:%M').time()))
        db.session.add(ConfirmedTrip(trip_request_id=2, customer_id=2, driver_id=2,
                                     confirmation_date=datetime.strptime('2021-01-02', '%Y-%m-%d').date(),
                                     confirmation_time=datetime.strptime('11:00', '%H:%M').time()))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_confirmed_trips(self):
        """ Test for getting all confirmed trips"""
        response = self.app.get('/trips/confirmed')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    def test_delete_confirmed_trip(self):
        """ Test for deleting confirmed trip."""
        response = self.app.delete('/trips/confirmed/2')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()