"""Unit tests for coordinator_service module."""

import unittest
from app import app, db
from models import PendingCustomerRegistration, PendingDriverRegistration

class CustomerRegistrationsTestCase(unittest.TestCase):
    """Unit tests for customer registration routes."""
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(PendingCustomerRegistration(status='Pending',
                                                   username='user1', email='user1@example.com'))
        db.session.add(PendingCustomerRegistration(status='Approved',
                                                   username='user2', email='user2@example.com'))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_view_pending_customer_registrations(self):
        """Test view pending customer registrations."""
        response = self.app.get('/coordinators/pending-customer-registrations')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Pending')

    def test_view_specific_pending_customer_registration(self):
        """Test view specific pending customer registration."""
        response = self.app.get('/coordinators/pending-customer-registrations/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Pending')

    def test_view_specific_pending_customer_registration_not_found(self):
        """Test view specific pending customer registration not found."""
        response = self.app.get('/coordinators/pending-customer-registrations/11')
        self.assertEqual(response.status_code, 400)

    def test_reject_customer_registration(self):
        """Test reject customer registration."""
        response = self.app.put('/coordinators/pending-customer-registrations/1/reject')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration rejected successfully!', data['message'])
        registration = PendingCustomerRegistration.query.get(1)
        self.assertEqual(registration.status, 'Rejected')

    def test_add_pending_customer_registration(self):
        """Test add pending customer registration."""
        response = self.app.post('/coordinators/pending-customer-registrations', json={
            'status': 'Pending',
            'username': 'user3',
            'email': ''})
        self.assertEqual(response.status_code, 201)

    def test_view_approved_customer_registrations(self):
        """Test view approved customer registrations."""
        response = self.app.get('/coordinators/approved-customer-registrations')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Approved')

    def test_view_rejected_customer_registrations(self):
        """Test view rejected customer registrations."""
        db.session.add(PendingCustomerRegistration(status='Rejected', username='user3',))
        db.session.commit()
        response = self.app.get('/coordinators/rejected-customer-registrations')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Rejected')

class DriverRegistrationsTestCase(unittest.TestCase):
    """Unit tests for driver registration routes."""
    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(PendingDriverRegistration(status='Pending', username='driver1',))
        db.session.add(PendingDriverRegistration(status='Approved', username='driver2',))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_view_pending_driver_registrations(self):
        """Test view pending driver registrations"""
        response = self.app.get('/coordinators/pending-driver-registrations')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Pending')

    def test_view_specific_pending_driver_registration(self):
        """Test view specific pending driver registration"""
        response = self.app.get('/coordinators/pending-driver-registrations/1')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'Pending')

    def test_view_specific_pending_driver_registration_not_found(self):
        """Test view specific pending driver registration not found"""
        response = self.app.get('/coordinators/pending-driver-registrations/11')
        self.assertEqual(response.status_code, 400)

    def test_add_pending_driver_registration(self):
        """Test add pending driver registration"""
        response = self.app.post('/coordinators/pending-driver-registrations', json={
            'status': 'Pending',
            'username': 'driver3',})
        self.assertEqual(response.status_code, 201)

    def test_view_approved_driver_registrations(self):
        """Test view approved driver registrations"""
        response = self.app.get('/coordinators/approved-driver-registrations')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Approved')

    def test_view_rejected_driver_registrations(self):
        """Test view rejected driver registrations"""
        db.session.add(PendingDriverRegistration(status='Rejected', username='driver3'))
        db.session.commit()
        response = self.app.get('/coordinators/rejected-driver-registrations')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'Rejected')

    def test_reject_driver_registration(self):
        """Test reject driver registration"""
        response = self.app.put('/coordinators/pending-driver-registrations/1/reject')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration rejected successfully!', data['message'])
        registration = PendingDriverRegistration.query.get(1)
        self.assertEqual(registration.status, 'Rejected')

if __name__ == '__main__':
    unittest.main()