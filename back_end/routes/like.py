from flask import Blueprint, request, jsonify
from back_end.models import User, Post  # Import User and Post models
from back_end.database import Session


like_bp = Blueprint('like', __name__)

@like_bp.route('/like', methods=['POST'])
def like_post():
    data = request.json
    if not data or 'post_id' not in data or 'user_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']
    post_id = data['post_id']

    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    if post_id in user.like_list:
        return jsonify({'message': 'Post already liked by user'}), 409  # Conflict status code

    user.like_list.append(post_id)
    post.likes += 1

    Session.commit()
    return jsonify({'message': 'Post liked successfully'}), 200

@like_bp.route('/cancel_like', methods=['POST'])
def cancel_like():
    data = request.json
    if not data or 'post_id' not in data or 'user_id' not in data:
        return jsonify({'message': 'Missing data'}), 400

    user_id = data['user_id']
    post_id = data['post_id']

    user = User.query.get(user_id)
    post = Post.query.get(post_id)

    if not user:
        return jsonify({'message': 'User not found'}), 404
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    if post_id in user.like_list:
        user.like_list.remove(post_id)
        post.likes -= 1
        Session.commit()
        return jsonify({'message': 'Like removed successfully'}), 200
    else:
        return jsonify({'message': 'Like not found for this user and post'}), 404