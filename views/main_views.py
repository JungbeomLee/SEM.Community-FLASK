from flask import Blueprint, render_template, request, flash
from dotenv import load_dotenv
from encryption import myDES
import os
import pymysql

bp = Blueprint('main', __name__, url_prefix='/')

load_dotenv()

ivT = os.environ.get("IV")
database_pwd = os.environ.get("DAKTEABYASE")
register_pwd = os.environ.get("REKGIESTYER")

register_db = pymysql.connect(
    host=   "localhost",
    user=   "root", 
    passwd= database_pwd, 
    db=     "register_db", 
    charset="utf8"
  )

cursor = register_db.cursor(pymysql.cursors.DictCursor)

# custom error page
@bp.app_errorhandler(404)
def not_found_error(error):
  return render_template('page404.html'), 404

# main page
@bp.route('/')
def hi() :
  return render_template('index.html')

# my NEW register page
@bp.route('/register', methods=['GET','POST'])
def register() :

  pwd_key = myDES(register_pwd, ivT)

  if request.method == 'POST' and 'userid' in request.form and 'username' in request.form and 'email' in request.form and 'password' in request.form and 'profile' in request.form and 're_password' in request.form:
    
    user_id = request.form['userid']
    user_name = request.form['username']
    email = request.form['email'].lower()
    password = request.form['password']
    re_password = request.form['re_password']
    user_profile = request.form['profile']
    
    cursor.execute("SELECT email FROM users WHERE email=% s", email)
    email_compare = cursor.fetchone()

    # already signed email check code & unmatch password check
    if(email_compare) :

      flash('Already Signed up Email')

    elif(password != re_password) :

      flash('Unmatch password!')

    else :

      password = pwd_key.enc(password)
      cursor.execute('INSERT INTO users (id, name, email, password, profile) VALUES (% s, % s, % s, % s, % s)', (id, name, email, password, profile))
      register_db.commit()
      flash('Sign up Completed!')
      
      del password, user_id, user_name, email, re_password, user_profile, email_compare

      return render_template('index.html')
      
      
  return render_template('register.html')

