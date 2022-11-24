from flask import Blueprint, request, session
from views.utils.check_token import CHECK_TOKEN
from views.utils.env_var import database_pwd, jwt_secret_key
import pymysql
import jwt

bp = Blueprint('flask_own_user_nickname_check', __name__, url_prefix='/user/own_user')
   
@bp.route('/ownuserchecknickname', methods=['POST'])
@CHECK_TOKEN.check_for_token
def user() :
    # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "sebuung_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)
    # --------------------------------------------------------------------------------------------------------------
    # nickname duplicate check
    if request.method == 'POST' and 'user_nickname' in request.form :
        request_nickname = request.form['user_nickname'].lower()
        print(request_nickname)
        
        try : 
            cursor.execute("SELECT nickname FROM users WHERE nickname=%s", request_nickname)
            db_nickname = cursor.fetchone()['nickname'].lower()
            print(db_nickname)
        except :
            db_nickname = ''

        access_token = request.cookies.get('access_token')
        decode_access_token_emil = jwt.decode(access_token, jwt_secret_key, algorithms='HS256')['user_email']

        cursor.execute("SELECT nickname FROM users WHERE email=%s", decode_access_token_emil)
        user_nickname = cursor.fetchone()['nickname'].lower()
        print(user_nickname)

        if request_nickname == user_nickname :
            reps = {'nickname_duplicate_check' : 0}
        else :
            if request_nickname != db_nickname :
                reps = {'nickname_duplicate_check' : 1}
            else :
                reps = {'nickname_duplicate_check' : -1}
        return reps
        
