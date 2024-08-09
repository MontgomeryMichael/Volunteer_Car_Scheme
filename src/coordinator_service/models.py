"""
Model classes for the coordinator_service.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Coordinator(db.Model):
    """Class representing a coordinator."""
    coordinator_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15), nullable=False)

class PendingDriverRegistration(db.Model):
    """Class representing a pending driver registration."""
    registration_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='Pending')
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    license = db.Column(db.String(20))
    car_make = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    car_reg = db.Column(db.String(15))
    car_colour = db.Column(db.String(20))
    email = db.Column(db.String(50))
    mobile = db.Column(db.String(15))

    def to_dict(self):
        """Converts the object to a dictionary."""
        return {
            'registration_id': self.registration_id,
            'status': self.status,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'license': self.license,
            'car_make': self.car_make,
            'car_model': self.car_model,
            'car_reg': self.car_reg,
            'car_colour': self.car_colour,
            'email': self.email,
            'mobile': self.mobile
        }

class PendingCustomerRegistration(db.Model):
    """Class representing a pending customer registration."""
    registration_id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(10), nullable=False, default='Pending')
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address_line1 = db.Column(db.String(50))
    address_line2 = db.Column(db.String(50))
    town = db.Column(db.String(50))
    county = db.Column(db.String(50))
    postcode = db.Column(db.String(10))
    mobile = db.Column(db.String(15))
    email = db.Column(db.String(50))

    def to_dict(self):
        """Converts the object to a dictionary."""
        return {
            'registration_id': self.registration_id,
            'status': self.status,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'town': self.town,
            'county': self.county,
            'postcode': self.postcode,
            'mobile': self.mobile,
            'email': self.email
        }
