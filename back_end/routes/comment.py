from flask import Blueprint, request, jsonify
from back_end.models import Comment
from back_end.database import Session


comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['POST'])
def add_comment():
    data = request.json
    if not data or 'post_id' not in data or 'user_id' not in data or 'content' not in data:
        return jsonify({'message': 'Missing data'}), 400
    comment = Comment(post_id=data['post_id'], user_id=data['user_id'], content=data['content'])
    Session.add(comment)
    Session.commit()
    return jsonify({'message': 'Comment added successfully', 'comment_id': comment.cid}), 201

@comment_bp.route('/<int:cid>', methods=['PUT'])
def edit_comment(cid):
    data = request.json
    if not data or 'content' not in data:
        return jsonify({'message': 'Missing content in request'}), 400

    comment = Comment.query.get(cid)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    comment.content = data['content']
    Session.commit()
    return jsonify({'message': 'Comment updated successfully', 'comment_id': comment.cid}), 200

@comment_bp.route('/<int:cid>', methods=['DELETE'])
def delete_comment(cid):
    comment = Comment.query.get(cid)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    Session.delete(comment)
    Session.commit()
    return jsonify({'message': 'Comment deleted successfully', 'comment_id': cid}), 200