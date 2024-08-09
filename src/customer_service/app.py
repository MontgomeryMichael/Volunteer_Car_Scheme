""" Main application file for the customer service. """

from flask import Flask
from models import db, Customer
from routes import routes
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///customers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()
    if not Customer.query.filter_by(username='customer').first():
        db.session.add(Customer(first_name='Bill',
                                last_name='Buchanan',
                                username='customer',
                                address_line1='Richmond Street',
                                address_line2='',
                                town='Glasgow',
                                county='Glasgow',
                                postcode='G1 1XH',
                                mobile='1234567890',
                                email='customer@customer.com'))
        db.session.commit()

"""This is where the service starts."""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
