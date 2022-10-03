from flask import (Blueprint, render_template, request, flash, redirect, url_for, render_template, make_response)
from dotenv import load_dotenv
from flask_jwt_extended import (JWTManager, create_access_token, create_refresh_token)
import os
import pymysql
import bcrypt


bp = Blueprint('login', __name__, url_prefix='/')

jwt = JWTManager()

load_dotenv()

database_pwd = os.environ.get("DAKTEABYASE")
jwt_secret_key = os.environ.get("JWT_SECRET_KEY")
jwt_access_token_expires = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES'))
jwt_refresh_token_expires = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES'))

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
    password = request.form['password']

    # 입력받은 비번과 DB에 있는 비번 일치 검사
    cursor.execute("SELECT password FROM users WHERE email=% s", useremail)
    match_pwd = cursor.fetchone()
    if(match_pwd) : 
        check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'].encode())
        if(check_password==True) :
            flash('Login Successfuly')
            access_token_test = create_access_token(identity=useremail)
            refresh_token = create_refresh_token(identity=useremail)
            resp = make_response(redirect(url_for('login.login')))
            resp.set_cookie('access_token_cookie', access_token_test, max_age=jwt_access_token_expires)
            resp.set_cookie('refresh_token_cookie',refresh_token, max_age=jwt_refresh_token_expires)
            return resp
        else : 
            flash('Failed to Login')
            return redirect(url_for('login.login'))
    else :
        flash('Unsigned Email')
        return redirect(url_for('login.login'))
  else :
    return render_template('login.html')