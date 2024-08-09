""" Module defining models for the driver_service."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Driver(db.Model):
    """ Class to represent a driver."""
    driver_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    license = db.Column(db.String(20))
    car_make = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    car_reg = db.Column(db.String(15))
    car_colour = db.Column(db.String(20))
    email = db.Column(db.String(50))
    mobile = db.Column(db.String(15))

    def to_dict(self):
        """ Method to return a dictionary representation"""
        return {
            "driver_id": self.driver_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "license": self.license,
            "car_make": self.car_make,
            "car_model": self.car_model,
            "car_reg": self.car_reg,
            "car_colour": self.car_colour,
            "email": self.email,
            "mobile": self.mobile
        }
