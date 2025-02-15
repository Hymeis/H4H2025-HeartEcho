from flask import Blueprint, request, jsonify
from app import db
from models import Post

post_bp = Blueprint('post', __name__)

@post_bp.route('/', methods=['POST'])
def create_post():
    data = request.json
    post = Post(user_id=data['user_id'], content=data['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'}), 201

@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify([{'id': p.id, 'content': p.content, 'timestamp': p.timestamp} for p in posts])
