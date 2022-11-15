from flask import Blueprint, request, session
from views.utils.check_token import CHECK_TOKEN
from dotenv import load_dotenv
from views.utils.env_var import database_pwd, jwt_secret_key
import pymysql
import jwt


load_dotenv('../env')

bp = Blueprint('flask_own_user_changedatapost', __name__, url_prefix='/user/own_user')
   
@bp.route('/changedatapost', methods=['POST'])
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
    
    update = False

    # update user data
    if request.method == 'POST' and 'user_nickname' in request.form and 'user_profile' in request.form:
        user_nickname = request.form['user_nickname']
        user_profile = request.form['user_profile']
        
        access_token = request.cookies.get('access_token')
        decode_access_token_emil = jwt.decode(access_token, jwt_secret_key, algorithms='HS256')['user_email']

        cursor.execute("UPDATE users SET nickname=%s WHERE email=%s", (user_nickname, decode_access_token_emil))
        register_db.commit()
        cursor.execute("UPDATE users SET profile_text=%s WHERE email=%s", (user_profile, decode_access_token_emil))
        register_db.commit()
        register_db.close()

        update = True

        reps = {'update' : update}
        return reps
        
    # --------------------------------------------------------------------------------------------------------------
    # nickname duplicate check
    if request.method == 'POST' and 'user_nickname' in request.form :
        request_nickname = request.form['user_nickname'].lower()
        
        try : 
            cursor.execute("SELECT nickname FROM users WHERE nickname=%s", request_nickname)
            db_nickname = cursor.fetchone()['nickname'].lower()
        except :
            db_nickname = ''

        access_token = request.cookies.get('access_token')
        decode_access_token_emil = jwt.decode(access_token, jwt_secret_key, algorithms='HS256')['user_email']

        cursor.execute("SELECT nickname FROM users WHERE email=%s", decode_access_token_emil)
        user_nickname = cursor.fetchone()['nickname'].lower()

        if request_nickname == user_nickname :
            reps = {'nickname_duplicate_check' : 0}
        else :
            if request_nickname != db_nickname :
                reps = {'nickname_duplicate_check' : 1}
            else :
                reps = {'nickname_duplicate_check' : -1}
        return reps
        
