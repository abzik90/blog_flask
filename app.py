from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from security.config import JWT_KEY, DB_URI

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

jwt = JWTManager(app)
db = SQLAlchemy(app)

from api.user_controller import users_bp
app.register_blueprint(users_bp, url_prefix='/api/v1/')
from api.post_controller import posts_bp
app.register_blueprint(posts_bp, url_prefix="/api/v1/")