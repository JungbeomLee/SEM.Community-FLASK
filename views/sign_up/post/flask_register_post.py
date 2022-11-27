from flask import Blueprint, request
import bcrypt
import pymysql
from ...utils.env_var import database_pwd


bp = Blueprint('flask_register_post', __name__, url_prefix='/register')

@bp.route('/post', methods=['POST'])
def register_post() :
  if request.method == 'POST' and 'username' in request.form and 'useremail' in request.form and 'usernickname' in request.form and 'password' in request.form and 'profile' in request.form and 're_password' in request.form:

    user_name = request.form['username']
    useremail = request.form['useremail'].lower()
    password = request.form['password']
    user_profile = request.form['profile']
    user_nickname = request.form['usernickname']

    email_compare_check = False
    signUp_check = False
    post_data_check = True

    reps = {'email_compare_check' : email_compare_check, 'signUp_check' : signUp_check, 'post_data_check' : post_data_check}


    # connect mysql DataBase
    register_db = pymysql.connect(
          host=   "localhost",
          user=   "root", 
          passwd= database_pwd, 
          db=     "sebuung_db", 
          charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)
    
    cursor.execute("SELECT email FROM users WHERE email=% s", useremail)
    email_compare = cursor.fetchone()

    # already signed email check code & unmatch password check
    if(email_compare) :
      register_db.close()
      email_compare_check = True
      reps['email_compare_check'] = email_compare_check

      return reps
    else :
      signUp_check = True
      reps['signUp_check'] = signUp_check
      password = (bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')

      cursor.execute('INSERT INTO users (name, nickname, email, password, profile_text) VALUES (% s, %s, % s, % s, % s)', (user_name, user_nickname,useremail, password, user_profile))
      register_db.commit()
      register_db.close()

      return reps
  else :    
    post_data_check = False
    reps['post_data_check'] = post_data_check

    return reps