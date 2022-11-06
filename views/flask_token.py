from flask import Blueprint, request
from .utils.env_var import jwt_secret_key
from .utils.check_token import CHECK_TOKEN
import jwt

bp = Blueprint('flask_token', __name__, url_prefix='/')

@bp.route('/token')
@CHECK_TOKEN.check_for_token
def token():
    refresh_token = request.cookies.get('refresh_token')
    decode_refresh_token_email = jwt.decode(refresh_token, jwt_secret_key, algorithms='HS256')['user_email']
    
    return decode_refresh_token_email
