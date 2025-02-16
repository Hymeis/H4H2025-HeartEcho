from flask import Blueprint, request, jsonify
from back_end.models import Post
from back_end.database import Session


post_bp = Blueprint('post', __name__)

@post_bp.route('/', methods=['POST'])
def create_post():
    session = Session()
    data = request.json
    if not data or 'user_id' not in data or 'title' not in data or 'content' not in data or 'tag' not in data or 'user_nickname' not in data:
        return jsonify({'message': 'Missing required data'}), 400
    post = Post(
        user_id=data['user_id'],
        title=data['title'],
        content=data['content'],
        tag=data['tag'],
        user_nickname=data['user_nickname']
    )
    session.add(post)
    session.commit()
    return jsonify({'message': 'Post created successfully', 'post_id': post.pid}), 201

@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
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
            'timestamp': post.timestamp.isoformat() # Convert datetime to ISO string for JSON
        }
        post_list.append(post_data)
    return jsonify({'posts': post_list}), 200

@post_bp.route('/<int:pid>', methods=['PUT'])
def edit_post(pid):
    data = request.json
    if not data or 'title' not in data or 'content' not in data or 'tag' not in data or 'user_nickname' not in data:
        return jsonify({'message': 'Missing required data for update'}), 400

    post = Post.query.get(pid)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    post.title = data['title']
    post.content = data['content']
    post.tag = data['tag']
    post.user_nickname = data['user_nickname']

    Session.commit()
    return jsonify({'message': 'Post updated successfully', 'post_id': post.pid}), 200

@post_bp.route('/<int:pid>', methods=['DELETE'])
def delete_post(pid):
    post = Post.query.get(pid)
    if not post:
        return jsonify({'message': 'Post not found'}), 404

    Session.delete(post)
    Session.commit()
    return jsonify({'message': 'Post deleted successfully', 'post_id': pid}), 200