from flask import (Blueprint, flash, make_response, redirect, url_for, render_template, session)
from ..utils.env_var import jwt_secret_key, jwt_access_token_expires, jwt_refresh_token_expires, database_pwd
from ..utils.check_token import CHECK_TOKEN

bp = Blueprint('flask_logout', __name__, url_prefix='/')

# login
@bp.route('/logout', methods=['GET'])
@CHECK_TOKEN.check_for_token
def logout() : 
    session.pop('user_email', None)

    resp = make_response(redirect(url_for('flask_main.main_page')))
    resp.set_cookie('access_token', '', expires=0)
    resp.set_cookie('refresh_token', '', expires=0)

    flash('Logout successfully')
    return resp