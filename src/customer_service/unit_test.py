""" Module contains unit tests for customer service. """

import unittest
from app import app,db
from models import Customer

class TestCustomerService(unittest.TestCase):
    """Unit tests for customer service."""
    def setUp(self):
        self.app = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()
            new_customer = Customer(username='existingcustomer',
                                    first_name='John',
                                    last_name='Doe',
                                    address_line1='1 High Street',
                                    address_line2='Anytown',
                                    town='Anytown',
                                    county='Anycounty',
                                    postcode='AB12 3CD',
                                    mobile='1234567890',
                                    email='something@something')
            db.session.add(new_customer)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_customer(self):
        """Test creating a customer profile."""
        response = self.app.post('/register', json={
            'username': 'newcustomer',
            'first_name': 'Luke',
            'last_name': 'Skywalker',
            'address_line1': '2 High Street',
            'address_line2': 'Anytown',
            'town': 'Anytown',
            'county': 'Anycounty',
            'postcode': 'CD21 3AB',
            'mobile': '0987654321',
            'email': 'something@something'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Customer profile created successfully!', response.json['message'])

    def test_get_customer(self):
        """Test getting a customer profile."""
        response = self.app.get('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['customer_id'], 1)

    def test_get_customer_by_username(self):
        """Test getting a customer profile using their username."""
        response = self.app.get('/customers/details/existingcustomer')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['username'], 'existingcustomer')

    def test_get_all_customers(self):
        """Test getting all customer profiles."""
        response = self.app.get('/customers/all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_update_customer(self):
        """Test updating a customer profile."""
        response = self.app.put('/customers/1', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'address_line1': '2 High Street',
            'address_line2': 'Anytown',
            'town': 'Anytown',
            'county': 'Anycounty',
            'postcode': 'CD21 3AB',
            'mobile': '0987654321',
            'email': 'something@something'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Customer profile updated successfully!', response.json['message'])

    def test_delete_customer(self):
        """Test deleting a customer profile."""
        response = self.app.delete('/customers/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Customer profile deleted successfully!', response.json['message'])

    def test_get_customer_not_found(self):
        """Test getting a customer profile that does not exist."""
        response = self.app.get('/customers/11')
        self.assertEqual(response.status_code, 404)

    def test_update_customer_not_found(self):
        """Test updating a customer profile that does not exist."""
        response = self.app.put('/customers/11', json={
            'first_name': 'Jane',
            'last_name': 'Doe',
            'address_line1': '2 High Street',
            'address_line2': 'Anytown',
            'town': 'Anytown',
            'county': 'Anycounty',
            'postcode': 'CD21 3AB',
            'mobile': '0987654321',
            'email': 'something@something'
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
