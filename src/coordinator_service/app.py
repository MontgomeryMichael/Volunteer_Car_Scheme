"""
Entry point of the application. 
Creates the Flask app, initializes the database, and registers the routes.
"""

from flask import Flask
from models import Coordinator, db
from routes import coordinator_routes
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coordinators.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

app.register_blueprint(coordinator_routes)

with app.app_context():
    db.create_all()
    if not Coordinator.query.filter_by(first_name='Connor').first():
        db.session.add(Coordinator(username='admin',
                                   first_name='Connor', last_name='MacLeod',
                                   email='vcs@fakeemail.com', phone='07807807707'))
        db.session.commit()

"""This is where the service starts."""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)