from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_flask_exporter import PrometheusMetrics
from datetime import datetime
import os
import requests
import logging
from sqlalchemy.exc import OperationalError
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


# MySQL database connection configuration
DB_USER = 'root'
DB_PASS = 'Dishani99'
DB_HOST = 'localhost'
DB_NAME = 'riders_db'
DB_PORT = 3306

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Enable logging and storing it in app.log and DB
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
    handlers=[
        logging.FileHandler("app.log"),     # logs to file
        logging.StreamHandler()             # logs to console
    ]
)

class Log(db.Model):
    __tablename__ = 'logs_riders'
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def log_request_info():
    msg = f"Incoming {request.method} request: {request.path}"
    app.logger.info(msg)
    try:
        new_log = Log(level="INFO", message=msg)
        db.session.add(new_log)
        db.session.commit()
    except Exception as e:
        app.logger.warning(f"Could not log to DB: {e}")
        db.session.rollback()

# Rate Limiting (to prevent overload)
limiter = Limiter(get_remote_address, app=app, default_limits=["20 per minute"])

# Prometheus Monitoring (adds /metrics endpoint)
metrics = PrometheusMetrics(app)


#Database Model
class Rider(db.Model):
    __tablename__ = 'riders'
    rider_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {'rider_id': self.rider_id, 'name': self.name, 'email': self.email, 'phone': self.phone, 'created_at': self.created_at.isoformat()}

# API Endpoints (CRUD + Health)

# Get All Riders
@app.route('/v1/riders', methods=['GET'])
@limiter.limit("20 per minute")
def list_riders():
    try:
        riders = Rider.query.order_by(Rider.rider_id).all()
        return jsonify([r.to_dict() for r in riders])
    except OperationalError as e:
        app.logger.error(f"Database connection failed: {e}")
        return jsonify({'error': 'Database unavailable', 'details': str(e)}), 503

# Create a New Rider
@app.route('/v1/riders', methods=['POST'])
@limiter.limit("10 per minute")
def create_rider():
    try:
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        if not name or not email:
            return jsonify({'error':'name and email required'}), 400
        if Rider.query.filter_by(email=email).first():
            return jsonify({'error':'rider with this email already exists'}), 409
        r = Rider(name=name, email=email, phone=phone)
        db.session.add(r)
        db.session.commit()
        return jsonify(r.to_dict()), 201
    except BadRequest:
        return jsonify({'error': 'Invalid JSON body'}), 400
    except OperationalError as e:
        app.logger.error(f"Database connection failed: {e}")
        return jsonify({'error': 'Database unavailable', 'details': str(e)}), 503
    except Exception as e:
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# Get a Single Rider by ID
@app.route('/v1/riders/<int:rider_id>', methods=['GET'])
def get_rider(rider_id):
    r = Rider.query.get(rider_id)
    if not r:
        return jsonify({'error':'not found'}), 404
    return jsonify(r.to_dict())

# Update Rider by ID
@app.route('/v1/riders/<int:rider_id>', methods=['PUT'])
def update_rider(rider_id):
    r = Rider.query.get(rider_id)
    if not r:
        return jsonify({'error':'not found'}), 404
    data = request.get_json() or {}
    r.name = data.get('name', r.name)
    r.email = data.get('email', r.email)
    r.phone = data.get('phone', r.phone)
    db.session.commit()
    return jsonify(r.to_dict())

# Delete Rider by ID
@app.route('/v1/riders/<int:rider_id>', methods=['DELETE'])
def delete_rider(rider_id):
    r = Rider.query.get(rider_id)
    if not r:
        return jsonify({'error':'not found'}), 404
    db.session.delete(r)
    db.session.commit()
    return jsonify({'message':'deleted'})

# Health Check Endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status':'ok'})

@app.route('/')
def home():
    return "Rider Microservice is running! Try /v1/riders or /health"


# inter-service call (Trip service)
@app.route('/v1/riders/<int:rider_id>/trips', methods=['GET'])
def get_rider_trips(rider_id):
    try:
        trip_service_url = f"http://localhost:5002/v1/trips?rider_id={rider_id}"
        response = requests.get(trip_service_url, timeout=5)
        trips_data = response.json() if response.status_code == 200 else []
        return jsonify({
            "rider_id": rider_id,
            "trips": trips_data
        })
    except Exception as e:
        return jsonify({"error": "Trip service unavailable", "details": str(e)}), 503


#Global Error Handlers
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled Exception: {e}")
    return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'error': 'Invalid JSON body'}), 400


#Run the Application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5001, debug=True)