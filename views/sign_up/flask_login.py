from flask import (Blueprint, render_template, request, flash, redirect, url_for, render_template, make_response, session, jsonify, json)
from ..utils.env_var import jwt_secret_key, jwt_access_token_expires, jwt_refresh_token_expires, database_pwd
import pymysql
import jwt
import bcrypt
import datetime

bp = Blueprint('flask_login', __name__, url_prefix='/')

# login
@bp.route('/login', methods=['GET','POST'])
def login() : 
  if request.method == 'POST' and 'useremail' in request.form and 'password' in request.form:
    # form에서 받은 정보 변수에 저장
    useremail = request.json['useremail']
    print(useremail)
    password = str(request.json['password'])

    # connect mysql DataBase
    register_db = pymysql.connect(
          host=   "localhost",
          user=   "root", 
          passwd= database_pwd, 
          db=     "register_db", 
          charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)

    # 입력받은 비번과 DB에 있는 비번 일치 검사
    cursor.execute("SELECT password FROM users WHERE email=% s", useremail)
    match_pwd = cursor.fetchone()
    
    if(match_pwd) : 
        check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'])
        if(check_password==True) :
            register_db.close()
            
            # create access/refresh token
            access_token = jwt.encode({
              'user_email' : useremail,
              'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_access_token_expires)
            }, jwt_secret_key, algorithm='HS256')
            refresh_token = jwt.encode({
              'user_email' : useremail,
              'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=jwt_refresh_token_expires)
            }, jwt_secret_key, algorithm='HS256')
            
            # set session
            session['user_email'] = useremail

            # set cookies
            reps = make_response(redirect(url_for('flask_main.main_page')))
            reps.set_cookie('access_token', access_token)
            reps.set_cookie('refresh_token', refresh_token)
            flash('Login Successfuly')
            return reps
        else : 
            flash('Failed to Login')
            register_db.close()
            
            return redirect(url_for('flask_login.login'))
    else :
        flash('Unsigned Email')
        register_db.close()
        
        return redirect(url_for('flask_login.login'))
  else :
    return render_template('login.html')

@bp.route('/login/post', methods=['POST'])
def login_post() :
  if request.method == 'POST':
    # form에서 받은 정보 변수에 저장
    useremail = request.form['useremail']
    password = str(request.form['password'])

    # connect mysql DataBase
    register_db = pymysql.connect(
          host=   "localhost",
          user=   "root", 
          passwd= database_pwd, 
          db=     "register_db", 
          charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)

    # 입력받은 비번과 DB에 있는 비번 일치 검사
    cursor.execute("SELECT password FROM users WHERE email=% s", useremail)
    match_pwd = cursor.fetchone()
    
    if(match_pwd) : 
        check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'])
        if(check_password==True) :
            register_db.close()

            # set session
            session['user_email'] = useremail

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
            reps = {'login' : True, 'access_token' : access_token, 'refresh_token' : refresh_token}
            return reps
