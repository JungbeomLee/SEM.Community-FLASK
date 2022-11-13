from flask import Blueprint, request, session
from views.utils.check_token import CHECK_TOKEN
from dotenv import load_dotenv
from views.utils.env_var import database_pwd
import pymysql


load_dotenv('../env')

bp = Blueprint('flask_own_user_changedatapost', __name__, url_prefix='/user/own_user')
   
@bp.route('/changedatapost', methods=['POST'])
@CHECK_TOKEN.check_for_token
def user() :
    if request.method == 'POST' and 'user_nickname' in request.form or 'user_profile' in request.form:
        user_nickname = request.form['user_nickname']
        user_profile = request.form['user_profile']
        
        own_user_email = session['user_email']
        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "sebuung_db", 
            charset="utf8"
        )
        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        cursor.execute("UPDATE users SET nickname=%s WHERE email=%s", (user_nickname, own_user_email))
        register_db.commit()
        cursor.execute("UPDATE users SET profile_text=%s WHERE email=%s", (user_profile, own_user_email))
        register_db.commit()
        register_db.close()

        reps = {'update' : True}

        return reps
    else :
        reps = {'update' : False}

        return reps
        
