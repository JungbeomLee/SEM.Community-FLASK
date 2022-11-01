from flask import Blueprint, render_template, request, flash, url_for, redirect
from ..utils.check_token import CHECK_TOKEN
from dotenv import load_dotenv
from ..utils.env_var import database_pwd, jwt_secret_key
import bcrypt
import jwt
import pymysql

load_dotenv('../env')

bp = Blueprint('flask_user', __name__, url_prefix='/')

@bp.route('/user/own_user', methods=['GET','POST'])
@CHECK_TOKEN.check_for_token
def user() :
    user_token = request.cookies.get('access_token')
    decode_user_token_email = jwt.decode(user_token, jwt_secret_key, algorithms='HS256')['user_email']

    # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "register_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)

    # create user_data dict variable
    # get user_data
    cursor.execute("SELECT name FROM users WHERE email=%s", decode_user_token_email)
    user_name = cursor.fetchone()['name']
    cursor.execute("SELECT profile FROM users WHERE email=%s", decode_user_token_email)
    user_profile = cursor.fetchone()['profile']
    cursor.execute("SELECT created_at FROM users WHERE email=%s", decode_user_token_email)
    user_created_at = cursor.fetchone()['created_at']
    # create user_data dict
    user_data = {'user_name' : user_name, 'user_profile' : user_profile, 'user_created_at' : user_created_at}

    route_name = request.args.get("name", user_name)

    # change password or profile POST or delete_userpost
    if request.method == 'POST' and 'password' in request.form or 'change_password' in request.form or 'change_profile' in request.form or 'delect_user' in request.form:

        # checkout password
        if request.method == 'POST' and 'password' in request.form :
            password = str(request.form['password'])
            
            cursor.execute("SELECT password FROM users WHERE email=%s", decode_user_token_email)
            match_pwd = cursor.fetchone()
            check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'])

            # if password same
            if(check_password == True) :
                flash('Comnfirmed password!')
                return render_template('user.html', pwd_check = True, user_data = user_data)
            else :
                flash('Unmatch password!')
                return redirect(url_for('flask_user.user'))

        # if get POST change_password
        if request.method == 'POST' and 'change_password' in request.form :
            change_password = str(request.form['change_password'])
            if(len(change_password) != 0) :
                cursor.execute("SELECT password FROM users WHERE email=%s", decode_user_token_email)
                match_pwd = cursor.fetchone()
                check_password = bcrypt.checkpw(change_password.encode('utf-8'), match_pwd['password'])

                # if new_password == old_password
                if(check_password == True) :
                    flash('Already using password!')
                    return redirect(url_for('flask_user.user'))
                else :
                    endcode_change_password = (bcrypt.hashpw(change_password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
                    cursor.execute("UPDATE users SET password=%s WHERE email=%s", (endcode_change_password, decode_user_token_email))
                    register_db.commit()
    
                    flash('UserData Change Completed!')
                    return redirect(url_for('flask_user.user'))

        # if get POST change_profile
        if request.method == 'POST' and 'change_profile' in request.form :
            change_profile = str(request.form['change_profile'])

            cursor.execute("UPDATE users SET profile=%s WHERE email=%s", (change_profile, decode_user_token_email))
            register_db.commit()

            flash('UserData Change Completed!')
            return redirect(url_for('flask_user.user'))

        # if get POST delete_user
        if request.method == 'POST' and 'delete_user' in request.form :
            flash('Are you sure really delete your account?')
            return render_template(really_delete=True)

    else :
        return render_template("user.html",name = route_name, user_data = user_data, user_name = user_name)
