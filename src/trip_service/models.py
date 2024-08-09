from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class TripRequest(db.Model):
    trip_request_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    destination = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    additional_passenger = db.Column(db.String(50))
    purpose = db.Column(db.String(300))
    status = db.Column(db.String(50), default='Pending')

    def to_dict(self):
        return {
            'trip_request_id': self.trip_request_id,
            'customer_id': self.customer_id,
            'date': self.date.strftime('%Y-%m-%d') if self.date else None,
            'time': self.time.strftime('%H:%M') if self.time else None,
            'destination': self.destination,
            'duration': self.duration,
            'additional_passenger': self.additional_passenger,
            'purpose': self.purpose,
            'status': self.status
        }

class ConfirmedTrip(db.Model):
    confirmed_trip_id = db.Column(db.Integer, primary_key=True)
    trip_request_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    confirmation_date = db.Column(db.Date, nullable=False)
    confirmation_time = db.Column(db.Time, nullable=False)

    def to_dict(self):
        return {
            'confirmed_trip_id': self.confirmed_trip_id,
            'trip_request_id': self.trip_request_id,
            'customer_id': self.customer_id,
            'driver_id': self.driver_id,
            'confirmation_date': self.confirmation_date.strftime('%Y-%m-%d') if self.confirmation_date else None,
            'confirmation_time': self.confirmation_time.strftime('%H:%M') if self.confirmation_time else None
        }