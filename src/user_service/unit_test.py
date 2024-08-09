""" Unit tests for the user service """

import unittest
from app import app, db
from models import User

class FlaskTestCase(unittest.TestCase):
    """ Unit tests for the user service"""
    def setUp(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            db.session.add(User(username='existingdriver',
                                password='driverpass', role='Driver'))
            db.session.add(User(username='existingcustomer',
                                password='customerpass', role='Customer'))
            db.session.add(User(username='existingcoordinator',
                                password='coordinatorpass', role='Coordinator'))
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_with_valid_roles(self):
        """ Test for registering a user."""
        with self.app.app_context():
            response_driver = self.client.post('/register', json={
                'username': 'testdriver',
                'password': 'testpass',
                'role': 'driver'
            })
            self.assertEqual(response_driver.status_code, 201)
            self.assertIn('User registered successfully!', response_driver.json['message'])

            response_customer = self.client.post('/register', json={
            'username': 'testcustomer',
            'password': 'testpass',
            'role': 'customer'
             })
            self.assertEqual(response_customer.status_code, 201)
            self.assertIn('User registered successfully!', response_customer.json['message'])

    def test_register_with_invalid_role(self):
        """ Test for registering a user with invalid role."""
        with self.app.app_context():
            response = self.client.post('/register', json={
                'username': 'testcoordinator',
                'password': 'testpass',
                'role': 'coordinator'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid role for registration', response.json['message'])

    def test_login_with_valid_roles(self):
        """ Test for logging in a user."""
        with self.app.app_context():
            response_driver = self.client.post('/login', json={
                'username': 'existingdriver',
                'password': 'driverpass'
            })
            self.assertEqual(response_driver.status_code, 200)
            self.assertIn('Login successful!', response_driver.json['message'])

            response_customer = self.client.post('/login', json={
                'username': 'existingcustomer',
                'password': 'customerpass'
            })
            self.assertEqual(response_customer.status_code, 200)
            self.assertIn('Login successful!', response_customer.json['message'])

            response_coordinator = self.client.post('/login', json={
                'username': 'existingcoordinator',
                'password': 'coordinatorpass'
            })
            self.assertEqual(response_coordinator.status_code, 200)
            self.assertIn('Login successful!', response_coordinator.json['message'])

    def test_update_role_to_valid_roles(self):
        """ Test for updating a user role."""
        with self.app.app_context():
            self.client.post('/register', json={
                'username': 'roleupdateuser',
                'password': 'rolepass',
                'role': 'customer'  
            })
            user = User.query.filter_by(username='roleupdateuser').first()

            response = self.client.put(f'/users/{user.user_id}/roles', json={
                'role': 'driver'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('User role updated successfully!', response.json['message'])

if __name__ == '__main__':
    unittest.main()