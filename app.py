from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask_cors import CORS  # Import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all domains
CORS(app)  # This will allow all origins to access the Flask app

# Set up PostgreSQL connection using SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://sample_9er3_user:p3G9Vnf662te02ZKSYNSzu4ZstzAls4K@dpg-ct7l2fij1k6c73cj4o3g-a.oregon-postgres.render.com/sample_9er3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define User model for the registration table
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

# Create the tables (only necessary the first time)
with app.app_context():
    db.create_all()

# Endpoint to register a user
@app.route('/', methods=['POST'])
def register():
    # Get data from request
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validation
    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Check if the email is already registered
    existing_user = users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'Email already registered'}), 400

    # Hash the password
    hashed_password = generate_password_hash(password)

    # Create a new user
    new_user = users(username=username, email=email, password=password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Failed to register user', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
