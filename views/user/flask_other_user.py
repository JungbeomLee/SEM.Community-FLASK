from flask import Blueprint, render_template, request
from ..utils.check_token import CHECK_TOKEN
from dotenv import load_dotenv
from ..utils.env_var import database_pwd
import pymysql

load_dotenv('../env')

bp = Blueprint('flask_other_user', __name__, url_prefix='/')

@bp.route('/user/<route_user_nickname>', methods=['GET','POST'])
def other_user(route_user_nickname) :
    # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "register_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)
    
    # 입력받은 route_user_nickname이 실제 가입 유저인지 확인
    cursor.execute("SELECT name FROM users WHERE name=%s", route_user_nickname)
    try : 
        check_route_user_nickname = cursor.fetchone()['name']

        if check_route_user_nickname :
            cursor.execute("SELECT email FROM users WHERE name=%s", route_user_nickname)
            route_search_user_email = cursor.fetchone()['email']

            # create user_data dict variable
            # get user_data
            cursor.execute("SELECT name FROM users WHERE email=%s", route_search_user_email)
            other_user_name = cursor.fetchone()['name']
            cursor.execute("SELECT profile FROM users WHERE email=%s", route_search_user_email)
            user_profile = cursor.fetchone()['profile']
            cursor.execute("SELECT created_at FROM users WHERE email=%s", route_search_user_email)
            user_created_at = cursor.fetchone()['created_at']
            # create user_data dict
            user_data = {'user_name' : other_user_name, 'user_profile' : user_profile, 'user_created_at' : user_created_at}

            route_name = request.args.get("name", other_user_name)
            return render_template("other_user.html", name = route_name, other_user_data = user_data, other_user_name = other_user_name)
            
    except :
        return render_template('page404.html')
