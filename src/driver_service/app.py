""" Module to run the driver service. """

from flask import Flask
from flask_cors import CORS
from models import Driver, db
from routes import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///drivers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()
    if not Driver.query.filter_by(username='driver').first():
        db.session.add(Driver(first_name='John',
                                last_name='Doe',
                                username='driver',
                                license='1234567890',
                                car_make='Toyota',
                                car_model='Yaris',
                                car_reg='123456',
                                car_colour='Blue',
                                email='something@something.com',
                                mobile='1234567890'))
        db.session.commit()

"""This is where the service starts."""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)