from flask import Blueprint, make_response
from flask_jwt_extended import (JWTManager, get_jwt_identity, jwt_required)

bp = Blueprint('user', __name__, url_prefix='/')
jwt = JWTManager()

# jwt_required() error page
def unauthorized_response():
    return make_response("there is no access token", 401)

# catch jwt_required() error
@jwt.unauthorized_loader
def unauthorized_callback(callback):
    return unauthorized_response()

@bp.route('/user', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return current_user
