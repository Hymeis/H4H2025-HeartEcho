from flask import Blueprint, request, jsonify
from app import db
from back_end.db.models import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Login successful'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401
