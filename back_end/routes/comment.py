from flask import Blueprint, request, jsonify
from back_end.dao.models import Comment, User, Post
from back_end.dao.db_client import db_session

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['POST'])
def add_comment():
    data = request.json
    # Check for required fields
    if not data or 'post_id' not in data or 'user_id' not in data or 'content' not in data or 'comment_from' not in data:
        return jsonify({'message': 'Missing required data'}), 400

    # Create the comment
    comment = Comment(
        post_id=data['post_id'],
        user_id=data['user_id'],
        content=data['content'],
        comment_from=data['comment_from']  # Add comment_from field
    )
    db_session.add(comment)
    db_session.commit()

    # Update the Post's comment_list (only for direct comments)
    if data['comment_from'] == -1:  # Only add to Post's comment_list if it's a direct comment
        post = db_session.query(Post).get(data['post_id'])
        if post:
            post.comment_list = post.comment_list + [comment.cid] if post.comment_list else [comment.cid]
            db_session.commit()

    return jsonify({'message': 'Comment added successfully', 'comment_id': comment.cid}), 201

# @comment_bp.route('/<int:cid>', methods=['PUT'])
# def edit_comment(cid):
#     data = request.json
#     if not data or 'content' not in data:
#         return jsonify({'message': 'Missing content in request'}), 400
#
#     comment = db_session.query(Comment).get(cid)
#     if not comment:
#         return jsonify({'message': 'Comment not found'}), 404
#
#     comment.content = data['content']
#     db_session.commit()
#     return jsonify({'message': 'Comment updated successfully', 'comment_id': comment.cid}), 200

@comment_bp.route('/', methods=['DELETE'])
def delete_comment():
    data = request.json
    cid = data['cid']
    comment = db_session.query(Comment).get(cid)
    if not comment:
        return jsonify({'message': 'Comment not found'}), 404

    # Recursively delete child comments (threaded comments)
    def delete_child_comments(comment_id):
        child_comments = db_session.query(Comment).filter_by(comment_from=comment_id).all()
        for child in child_comments:
            delete_child_comments(child.cid)  # Recursively delete nested comments

            # Delete the child comment
            db_session.delete(child)
        db_session.commit()

    # Delete all child comments
    delete_child_comments(cid)

    # Remove the comment ID from the Post's comment_list (only for direct comments)
    if comment.comment_from == -1:  # Only remove from Post's comment_list if it's a direct comment
        post = db_session.query(Post).get(comment.post_id)
        if post and post.comment_list:
            post.comment_list = [comment_id for comment_id in post.comment_list if comment_id != cid]
            db_session.commit()

    # Delete the main comment
    db_session.delete(comment)
    db_session.commit()

    return jsonify({'message': 'Comment and its thread deleted successfully', 'comment_id': cid}), 200


@comment_bp.route('/query', methods=['GET'])
def query_comments():
    data = request.json
    # Get query parameters
    post_id = data['post_id']
    comment_from = data['comment_from']

    if post_id is None or comment_from is None:
        return jsonify({'message': 'Missing post_id or comment_from in query parameters'}), 400

    # Query comments based on post_id and comment_from
    comments = db_session.query(Comment).filter_by(post_id=post_id, comment_from=comment_from).all()

    # Prepare response
    comment_list = []
    for comment in comments:
        comment_data = {
            'cid': comment.cid,
            'post_id': comment.post_id,
            'user_id': comment.user_id,
            'content': comment.content,
            'likes': comment.likes,
            'comment_from': comment.comment_from,
            'timestamp': comment.timestamp.isoformat()
        }
        comment_list.append(comment_data)

    return jsonify({'comments': comment_list}), 200


# @comment_bp.route('/<int:cid>/like', methods=['POST'])
# def like_comment(cid):
#     data = request.json
#     if not data or 'user_id' not in data:
#         return jsonify({'message': 'Missing user_id in request'}), 400
#
#     # Fetch the comment
#     comment = db_session.query(Comment).get(cid)
#     if not comment:
#         return jsonify({'message': 'Comment not found'}), 404
#
#     # Fetch the user
#     user = db_session.query(User).get(data['user_id'])
#     if not user:
#         return jsonify({'message': 'User not found'}), 404
#
#     # Check if the user has already liked the comment
#     if cid in user.like_list:
#         return jsonify({'message': 'User has already liked this comment'}), 400
#
#     # Increment the comment's like count
#     comment.likes += 1
#
#     # Add the comment ID to the user's like_list
#     user.like_list = user.like_list + [cid] if user.like_list else [cid]
#
#     # Commit changes to the database
#     db_session.commit()
#
#     return jsonify({'message': 'Comment liked successfully', 'comment_id': cid, 'likes': comment.likes}), 200