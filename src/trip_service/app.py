""" Trip Service main module """

from flask import Flask
from models import db
from routes import routes
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trips.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)
app.register_blueprint(routes)

with app.app_context():
    db.create_all()

"""This is where the service starts."""
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
