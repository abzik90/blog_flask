from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from datetime import datetime
from models.post import Posts, db

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Posts.query.all()
    return jsonify([post.to_dict_min() for post in posts])

@posts_bp.route('/posts/<int:post_id>', methods=['GET'])
@jwt_required()
def get_post(post_id):
    post = Posts.query.get_or_404(post_id)
    return  jsonify(post.to_dict())

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
    author = request.json.get("author", "")
    title = request.json.get("title", "")
    content = request.json.get("content", "")
    add_date = datetime.now()

    new_post = Posts(author= author, title=title, content=content, add_date=add_date)
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
