from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import text, or_
from datetime import datetime
from models.post import Posts, db
from models.user import User

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    sort_by = request.args.get('sort_by', 'add_date').lower()  # Default sort by date
    sort_order = request.args.get('sort_order', 'desc').lower()  # Default sort order ascending
    keyword = request.args.get('keyword', "")
    sort_by = "author_id" if sort_by == "author_id" else "title" if sort_by == "title" else "add_date"
    sort_order = "desc" if sort_order == "desc" else "asc"
    sort_column = text(f'{sort_by} {sort_order}')

    posts = Posts.query.filter(or_(Posts.title.ilike(f"%{keyword}%"), Posts.content.ilike(f"%{keyword}%"))).order_by(sort_column).paginate(page=page, per_page=per_page)

    return jsonify([post.to_dict_min() for post in posts])

@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Posts.query.get_or_404(post_id)
    return jsonify(post.to_dict())

@posts_bp.route('/posts/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@posts_bp.route('/posts/create', methods = ['POST'])
@jwt_required()
def create_post():
    author_username = get_jwt_identity()
    user = User.query.filter_by(username=author_username).first()
    if user:
        author_id = user.id
    title = request.json.get("title", "")
    content = request.json.get("content", "")
    add_date = datetime.now()

    new_post = Posts(author_id= author_id, title=title, content=content, add_date=add_date)
    if new_post.is_valid():
        db.session.add(new_post)
        db.session.commit()
        return jsonify({'message': 'Post created successfully'}), 200
    else:
        return jsonify({'message': 'Post data incorrect'}), 401

@posts_bp.route('/posts/update/<int:post_id>', methods = ['PUT'])
@jwt_required()
def update_post(post_id):
    post = Posts.query.get_or_404(post_id)
    updated_data = request.get_json()

    if not updated_data:
        return jsonify({'message': 'No data provided for update'}), 400

    post.title = updated_data.get('title', post.title)
    post.content = updated_data.get('content', post.content)

    db.session.commit()

    return jsonify({'message': 'Post updated successfully', 'post': post.to_dict()})