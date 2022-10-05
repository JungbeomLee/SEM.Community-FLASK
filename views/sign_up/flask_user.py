from pickle import TRUE
from flask import Blueprint, request
from ..check_token import CHECK_TOKEN
import sys

bp = Blueprint('flask_user', __name__, url_prefix='/')

@bp.route('/user', methods=['GET'])
@CHECK_TOKEN.check_for_token
def user():
    refresh_token = request.cookies.get('refresh_token_cookie')
    # Access the identity of the current user with get_jwt_identity
    current_user = 'hi'
    return current_user
