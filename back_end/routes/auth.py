from flask import Blueprint, request, jsonify
from back_end.dao.models import User
from back_end.dao.db_client import db_session  # Import the SQLAlchemy session

register_bp = Blueprint('register', __name__)

@register_bp.route('/', methods=['POST'])
def register_user():
    data = request.json  # Use request.json instead of request.json()
    email = data.get('email')  # Use .get() to safely access the key

    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Check if the email already exists
    existing_user = db_session.query(User).filter_by(email=email).first()

    if existing_user:
        # User already exists, return their uid
        return jsonify({'uid': existing_user.uid}), 200
    else:
        # Create a new user
        new_user = User(
            email=email,
            post_list=[],  # Default empty list for post_list
            like_list=[]   # Default empty list for like_list
        )
        db_session.add(new_user)
        db_session.commit()

        # Return the new user's ID
        return jsonify({'uid': new_user.uid}), 201