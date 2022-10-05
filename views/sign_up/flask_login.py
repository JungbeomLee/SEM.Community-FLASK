from flask import (Blueprint, render_template, request, flash, redirect, url_for, render_template, make_response)
from dotenv import load_dotenv
import jwt
import os
import pymysql
import bcrypt
import datetime

from views.sign_up.flask_user import user

bp = Blueprint('flask_login', __name__, url_prefix='/')

load_dotenv('../../env')

# get .env
database_pwd = os.environ.get("DAKTEABYASE")
jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
jwt_access_token_expires = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES"))
jwt_refresh_token_expires = int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES"))


# connect mysql DataBase
register_db = pymysql.connect(
    host=   "localhost",
    user=   "root", 
    passwd= database_pwd, 
    db=     "register_db", 
    charset="utf8"
)
cursor = register_db.cursor(pymysql.cursors.DictCursor)

# login
@bp.route('/login', methods=['GET','POST'])
def login() : 

  if request.method == 'POST' and 'useremail' in request.form and 'password' in request.form:
    
    useremail = request.form['useremail']
    password = str(request.form['password'])

    # 입력받은 비번과 DB에 있는 비번 일치 검사
    cursor.execute("SELECT password FROM users WHERE email=% s", useremail)
    match_pwd = cursor.fetchone()
    if(match_pwd) : 
        check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'])
        if(check_password==True) :
            flash('Login Successfuly')
            
            # create access/refresh token
            access_token = jwt.encode({
              'user_email' : useremail,
              'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_access_token_expires)
            }, jwt_secret_key, algorithm='HS256')
            refresh_token = jwt.encode({
              'user_email' : useremail,
              'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_refresh_token_expires)
            }, jwt_secret_key, algorithm='HS256')

            # set cookies
            reps = make_response(redirect(url_for('flask_main.main_page')))
            reps.set_cookie('access_token', access_token)
            reps.set_cookie('refresh_token', refresh_token)
            return reps
        else : 
            flash('Failed to Login')
            return redirect(url_for('flask_login.login'))
    else :
        flash('Unsigned Email')
        return redirect(url_for('flask_login.login'))
  else :
    return render_template('login.html')