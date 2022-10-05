from flask import Blueprint, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import os
import pymysql
import bcrypt


bp = Blueprint('flask_register', __name__, url_prefix='/')

load_dotenv()

database_pwd = os.environ.get("DAKTEABYASE")

register_db = pymysql.connect(
    host=   "localhost",
    user=   "root", 
    passwd= database_pwd, 
    db=     "register_db", 
    charset="utf8"
  )

cursor = register_db.cursor(pymysql.cursors.DictCursor)

# my NEW register page
@bp.route('/register', methods=['GET','POST'])
def register() :

  if request.method == 'POST' and 'username' in request.form and 'useremail' in request.form and 'password' in request.form and 'profile' in request.form and 're_password' in request.form:
    
    user_name = request.form['username']
    useremail = request.form['useremail'].lower()
    password = request.form['password']
    re_password = request.form['re_password']
    user_profile = request.form['profile']
    
    cursor.execute("SELECT email FROM users WHERE email=% s", useremail)
    email_compare = cursor.fetchone()
    print(email_compare)

    # already signed email check code & unmatch password check
    if(email_compare) :
      flash('Already Signed up Email')
      return redirect(url_for('flask_register.register'))
    elif(password != re_password) :
      flash('Unmatch password!')
      return redirect(url_for('flask_register.register'))
    else :
      password = (bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
      cursor.execute('INSERT INTO users (name, email, password, profile) VALUES (% s, % s, % s, % s)', (user_name, useremail, password, user_profile))
      register_db.commit()

      flash('Sign up Completed!')

      return redirect(url_for('flask_main.main_page'))
      
  return render_template('register.html')


