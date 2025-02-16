from flask import Blueprint, request, jsonify
from back_end.dao.models import Post, User
from back_end.dao.db_client import db_session
import time

post_bp = Blueprint('post', __name__)

def generate_pseudo_random_string(length=10, seed=None):
    """Generate a pseudo-random alphanumeric string using LCG."""
    CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    A = 1664525
    C = 1013904223
    M = 2**32

    # Use current time as seed if none is provided
    if seed is None:
        seed = int(time.time())

    result = []
    Xn = seed  # Initialize with seed

    for _ in range(length):
        Xn = (A * Xn + C) % M  # Apply LCG formula
        result.append(CHARSET[Xn % len(CHARSET)])  # Map to charset

    return "".join(result)

@post_bp.route('/', methods=['POST'])
def create_post():
    data = request.json
    if not data or 'user_id' not in data or 'title' not in data or 'content' not in data or 'tag' not in data not in data:
        return jsonify({'message': 'Missing required data'}), 400

    post = Post(
        user_id=data['user_id'],
        title=data['title'],
        content=data['content'],
        tag=data['tag'],
        user_nickname="Echo" + generate_pseudo_random_string(10)
    )
    db_session.add(post)
    db_session.commit()

    # Update the user's post_list
    user = db_session.query(User).get(data['user_id'])
    if user:
        user.post_list = user.post_list + [post.pid] if user.post_list else [post.pid]
        db_session.commit()

    return jsonify({'message': 'Post created successfully', 'post_id': post.pid}), 201

#
# @post_bp.route('/<int:pid>', methods=['PUT'])
# def edit_post(pid):
#     data = request.json
#     if not data or 'title' not in data or 'content' not in data or 'tag' not in data or 'user_nickname' not in data:
#         return jsonify({'message': 'Missing required data for update'}), 400
#
#     post = Post.query.get(pid)
#     if not post:
#         return jsonify({'message': 'Post not found'}), 404
#
#     post.title = data['title']
#     post.content = data['content']
#     post.tag = data['tag']
#     post.user_nickname = data['user_nickname']
#
#     db_session.commit()
#     return jsonify({'message': 'Post updated successfully', 'post_id': post.pid}), 200

@post_bp.route('/', methods=['DELETE'])
def delete_post():
    data = request.json
    pid = data['pid']
    post = db_session.query(Post).get(pid)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Remove the post ID from the user's post_list
    user = db_session.query(User).get(post.user_id)
    if user and user.post_list:
        user.post_list = [post_id for post_id in user.post_list if post_id != pid]
        db_session.commit()

    db_session.delete(post)
    db_session.commit()
    return jsonify({'message': 'Post deleted successfully', 'post_id': pid}), 200

@post_bp.route('/by_time', methods=['GET'])
def get_posts_by_time():
    posts = db_session.query(Post).order_by(Post.timestamp.desc()).limit(10).all()
    post_list = []
    for post in posts:
        post_data = {
            'pid': post.pid,
            'user_id': post.user_id,
            'title': post.title,
            'content': post.content,
            'tag': post.tag,
            'user_nickname': post.user_nickname,
            'likes': post.likes,
            'comment_list': post.comment_list,
            'timestamp': post.timestamp.isoformat()
        }
        post_list.append(post_data)
    return jsonify({'posts': post_list}), 200

@post_bp.route('/by_tag', methods=['GET'])
def get_posts_by_tag():
    data = request.json
    tag = data['tag']
    posts = db_session.query(Post).filter_by(tag=tag).order_by(Post.timestamp.desc()).limit(10).all()
    post_list = []
    for post in posts:
        post_data = {
            'pid': post.pid,
            'user_id': post.user_id,
            'title': post.title,
            'content': post.content,
            'tag': post.tag,
            'user_nickname': post.user_nickname,
            'likes': post.likes,
            'comment_list': post.comment_list,
            'timestamp': post.timestamp.isoformat()
        }
        post_list.append(post_data)
    return jsonify({'posts': post_list}), 200

@post_bp.route('/by_likes', methods=['GET'])
def get_posts_by_likes():
    posts = db_session.query(Post).order_by(Post.likes.desc()).limit(10).all()
    post_list = []
    for post in posts:
        post_data = {
            'pid': post.pid,
            'user_id': post.user_id,
            'title': post.title,
            'content': post.content,
            'tag': post.tag,
            'user_nickname': post.user_nickname,
            'likes': post.likes,
            'comment_list': post.comment_list,
            'timestamp': post.timestamp.isoformat()
        }
        post_list.append(post_data)
    return jsonify({'posts': post_list}), 200


@post_bp.route('/like', methods=['POST'])
def like_post():
    data = request.json
    user_id = data['user_id']
    pid = data['post_id']
    if user_id is None or pid is None:
        return jsonify({'message': 'Missing user_id or post_id in request'}), 400

    # Fetch the post
    post = db_session.query(Post).get(pid)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    # Fetch the user
    user = db_session.query(User).get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Check if the user has already liked the post
    if pid in user.like_list:
        return jsonify({'message': 'User has already liked this post'}), 400

    # Increment the post's like count
    post.likes += 1

    # Add the post ID to the user's like_list
    user.like_list = user.like_list + [pid] if user.like_list else [pid]

    # Commit changes to the database
    db_session.commit()

    return jsonify({'message': 'Post liked successfully', 'post_id': pid, 'likes': post.likes}), 200