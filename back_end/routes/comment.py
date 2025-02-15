from flask import Blueprint, request, jsonify
from app import db
from back_end.models import Comment

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['POST'])
def add_comment():
    data = request.json
    comment = Comment(post_id=data['post_id'], user_id=data['user_id'], content=data['content'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'}), 201
