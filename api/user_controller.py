from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from models.user import User, db

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@users_bp.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return  jsonify(user.to_dict())

@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@users_bp.route('/register', methods=['POST'])
def create_user():
    username = request.json.get('username', "")
    firstname = request.json.get('firstname', "")
    surname = request.json.get('surname', "")
    email = request.json.get('email', "")    
    password = request.json.get('password', "")

    new_user = User(username=username, firstname=firstname, surname=surname, email=email,password=password)
    if new_user.is_valid():
        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token,'message': 'User created successfully'}), 200
    else:
        return jsonify({'message': 'Invalid user information'}), 401

@users_bp.route('/login', methods=['POST'])
def authenticate_user():
    username = request.json.get('username', "")
    password = request.json.get('password', "")
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    return jsonify({'message': 'Invalid username or password'}), 401
