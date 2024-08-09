""" Unit tests for driver_service. """

import unittest
from app import app, db
from models import Driver

class TestDriverService(unittest.TestCase):
    """ Class to test the driver service. """
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
            new_driver = Driver(username='existingdriver',
                                first_name='John',
                                last_name='Doe',
                                license='AB123456',
                                car_make='Toyota',
                                car_model='Corolla',
                                car_reg='AB123CD',
                                car_colour='White',
                                email='something@something',
                                mobile='1234567890')
            db.session.add(new_driver)
            db.session.commit() 

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_driver(self):
        """ Test to create new driver profile."""
        response = self.app.post('/drivers', json={
            'username': 'newdriver',
            'first_name': 'Darth',
            'last_name': 'Vader',
            'license': 'CD654321',
            'car_make': 'Ford',
            'car_model': 'Focus',
            'car_reg': 'CD654EF',
            'car_colour': 'Black',
            'email': 'something@something',
            'mobile': '0987654321'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Driver profile created successfully!', response.json['message'])

    def test_get_driver(self):
        """ Test to get driver by driver_id."""
        response = self.app.get('/drivers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['driver_id'], 1)

    def test_get_driver_by_username(self):
        """ Test to get driver by username."""
        response = self.app.get('/drivers/details/existingdriver')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'existingdriver')

    def test_get_all_drivers(self):
        """ Test to get all drivers."""
        response = self.app.get('/drivers/all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_driver(self):
        """ Test to update driver profile."""
        response = self.app.put('/drivers/1', json={
            'first_name': 'Korben',
            'last_name': 'Dallas',
            'license': 'CD654321',
            'car_make': 'Ford',
            'car_model': 'Focus',
            'car_reg': 'CD654EF',
            'car_colour': 'Black',
            'email': 'something@something',
            'mobile': '0987654321'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Driver profile updated successfully!', response.json['message'])

    def test_delete_driver(self):
        """ Test to delete driver profile."""
        response = self.app.delete('/drivers/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Driver profile deleted successfully!', response.json['message'])

    def test_get_driver_not_found(self):
        """ Test to get driver when driver does not exist."""
        response = self.app.get('/drivers/2')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Driver not found', response.json['error'])

    def test_update_driver_not_found(self):
        """ Test to update driver profile when driver does not exist."""
        response = self.app.put('/drivers/2', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'license': 'CD654321',
            'car_make': 'Ford',
            'car_model': 'Focus',
            'car_reg': 'CD654EF',
            'car_colour': 'Black',
            'email': 'something@something',
            'mobile': '0987654321'
        })
        self.assertEqual(response.status_code, 404)
        if response.json is not None:
            self.assertIn('Driver not found', response.json['error'])
        else:
            self.fail("Expected JSON response not recieved")

    def test_delete_driver_not_found(self):
        """ Test to delete driver profile when driver does not exist."""
        response = self.app.delete('/drivers/2')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Driver not found', response.json['error'])

if __name__ == '__main__':
    unittest.main()