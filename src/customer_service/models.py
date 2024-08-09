"""Module defines the Customer model."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customer(db.Model):
    """Class representing a customer."""
    customer_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
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
            "customer_id": self.customer_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address_line1": self.address_line1,
            "address_line2": self.address_line2,
            "town": self.town,
            "county": self.county,
            "postcode": self.postcode,
            "mobile": self.mobile,
            "email": self.email
        }
