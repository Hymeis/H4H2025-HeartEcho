from flask import Blueprint, request, jsonify
from back_end.models import Post  # Import the Post model



query_bp = Blueprint('query', __name__)

@query_bp.route('/posts/search', methods=['GET'])
def search_posts():
    """
    Search posts based on time, tag, and order by likes or time.
    Supports filtering by tag and ordering by 'latest', 'oldest', or 'most_liked'.
    """
    tag = request.args.get('tag')
    order_by = request.args.get('order_by')  # 'latest', 'oldest', 'most_liked'

    query = Post.query

    if tag:
        query = query.filter(Post.tag == tag)

    if order_by == 'latest':
        query = query.order_by(Post.timestamp.desc())
    elif order_by == 'oldest':
        query = query.order_by(Post.timestamp.asc())
    elif order_by == 'most_liked':
        query = query.order_by(Post.likes.desc())
    else:
        query = query.order_by(Post.timestamp.desc()) # Default to latest if no order specified

    posts = query.all()

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
            'timestamp': post.timestamp.isoformat()  # Convert datetime to ISO string for JSON
        }
        post_list.append(post_data)

    return jsonify({'posts': post_list}), 200


@query_bp.route('/posts/tag/<string:tag>', methods=['GET'])
def get_posts_by_tag(tag):
    """
    Get posts by a specific tag.
    """
    posts = Post.query.filter(Post.tag == tag).all()

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


@query_bp.route('/posts/most_liked', methods=['GET'])
def get_most_liked_posts():
    """
    Get posts ordered by likes in descending order.
    You can use a query parameter 'limit' to specify the number of posts to return.
    """
    limit = request.args.get('limit', default=None, type=int) # Get limit from query params

    query = Post.query.order_by(Post.likes.desc())

    if limit:
        query = query.limit(limit)

    posts = query.all()

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


@query_bp.route('/posts/latest', methods=['GET'])
def get_latest_posts():
    """
    Get posts ordered by timestamp in descending order (latest first).
    You can use a query parameter 'limit' to specify the number of posts to return.
    """
    limit = request.args.get('limit', default=None, type=int) # Get limit from query params

    query = Post.query.order_by(Post.timestamp.desc()) # Latest first

    if limit:
        query = query.limit(limit)

    posts = query.all()

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

@query_bp.route('/posts/oldest', methods=['GET'])
def get_oldest_posts():
    """
    Get posts ordered by timestamp in ascending order (oldest first).
    You can use a query parameter 'limit' to specify the number of posts to return.
    """
    limit = request.args.get('limit', default=None, type=int) # Get limit from query params

    query = Post.query.order_by(Post.timestamp.asc()) # Oldest first

    if limit:
        query = query.limit(limit)

    posts = query.all()

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