from flask import Blueprint, request, jsonify
from app import db
from back_end.models import Like

like_bp = Blueprint('like', __name__)

@like_bp.route('/', methods=['POST'])
def like_post():
    data = request.json
    like = Like(post_id=data['post_id'], user_id=data['user_id'])
    db.session.add(like)
    db.session.commit()
    return jsonify({'message': 'Post liked successfully'}), 201
