from flask import Blueprint, request, session
from views.utils.check_token import CHECK_TOKEN
from dotenv import load_dotenv
from views.utils.env_var import database_pwd, jwt_secret_key
import pymysql
import bcrypt
import datetime
import jwt

load_dotenv('../env')

bp = Blueprint('flask_own_user_passwordpost', __name__, url_prefix='/user/own_user')

@bp.route('/passwordpost', methods=['POST'])
@CHECK_TOKEN.check_for_token
def user() :
    if request.method == 'POST' and 'password' in request.form :
        password = request.form['password']
        
        access_token = request.cookies.get('access_token')
        decode_access_token_emil = jwt.decode(access_token, jwt_secret_key, algorithms='HS256')['user_email']
        
        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "sebuung_db", 
            charset="utf8"
        )
        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        # checkout password
        if request.method == 'POST' and 'password' in request.form :
            password = str(request.form['password'])
                
            cursor.execute("SELECT password FROM users WHERE email=%s", decode_access_token_emil)
            match_pwd = cursor.fetchone()
            check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'])

            # if password same
            if(check_password == True) :
                password_check = True
                
                # create user_data dict variable
                # get user_data
                cursor.execute("SELECT name FROM users WHERE email=%s", decode_access_token_emil)
                user_name = cursor.fetchone()['name']

                cursor.execute("SELECT nickname FROM users WHERE email=%s", decode_access_token_emil)
                user_nickname = cursor.fetchone()['nickname']

                cursor.execute("SELECT profile_text FROM users WHERE email=%s", decode_access_token_emil)
                user_profile = cursor.fetchone()['profile_text']

                cursor.execute("SELECT created_at FROM users WHERE email=%s", decode_access_token_emil)
                user_created_at = cursor.fetchone()['created_at']

                cursor.execute('SELECT profile_image_name FROM users WHERE email=%s', decode_access_token_emil)
                profile_image_name = cursor.fetchone()['profile_image_name']
                register_db.close()

                cache_cracker = datetime.datetime.utcnow()
                profile_image_link = f'https://flask-user-image-storage.s3.ap-northeast-2.amazonaws.com/images/{profile_image_name}.jpg?{cache_cracker}'
                
                # create user_data dict
                reps = {'password_check' : password_check,
                        'user_name' : user_name, 
                        'user_nickname' : user_nickname,
                        'user_profile' : user_profile, 
                        'user_created_at' : user_created_at, 
                        'user_profile_image_link' : profile_image_link}

                return reps


            else :
                password_check = False
                reps = {'password_check' : password_check}

                return reps
