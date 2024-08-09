""" Module contains main app for the user service. """

from flask import Flask
from models import User, db
from routes import routes
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password='admin', role='Coordinator'))
        db.session.commit()
    if not User.query.filter_by(username='driver').first():
        db.session.add(User(username='driver', password='driver', role='Driver'))
        db.session.commit()
    if not User.query.filter_by(username='customer').first():
        db.session.add(User(username='customer', password='customer', role='Customer'))
        db.session.commit()

"""This is where the service starts."""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)