from flask import Blueprint, render_template, request, flash, url_for, redirect
from ...utils.check_token import CHECK_TOKEN
from ...utils.env_var import database_pwd, jwt_secret_key
import bcrypt
import jwt
import pymysql
import datetime


bp = Blueprint('flask_user_post', __name__, url_prefix='/user/own_user')

@bp.route('/change_user_data_post', methods=['POST'])
@CHECK_TOKEN.check_for_token
def user() :
    # change password or profile POST or delete_userpost
    if request.method == 'POST' :
        user_token = request.cookies.get('access_token')
        decode_user_token_email = jwt.decode(user_token, jwt_secret_key, algorithms='HS256')['user_email']
        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "register_db", 
            charset="utf8"
        )
        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        # if get POST change_nickname and change_profile
        change_nickname = str(request.form['change_nickname'])
        change_profile = str(request.form['change_profile'])

        cursor.execute("UPDATE users SET nickname=%s WHERE email=%s", (change_nickname, decode_user_token_email))
        register_db.commit()
            
        cursor.execute("UPDATE users SET profile_text=%s WHERE email=%s", (change_profile, decode_user_token_email))
        register_db.commit()
        register_db.close()

        flash('UserData Change Completed!')
        return redirect(url_for('flask_user.user'))


