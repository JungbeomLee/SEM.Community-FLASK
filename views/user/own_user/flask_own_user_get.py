from flask import Blueprint, render_template, request, flash, url_for, redirect
from ...utils.check_token import CHECK_TOKEN
from ...utils.env_var import database_pwd, jwt_secret_key
import bcrypt
import jwt
import pymysql
import datetime

bp = Blueprint('flask_user_get', __name__, url_prefix='/user/own_user')

@bp.route('/get', methods=['GET'])
@CHECK_TOKEN.check_for_token
def user() :
    # change password or profile GET
    if request.method == 'GET' :

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
        cursor.execute("SELECT user_num FROM users WHERE email=%s", decode_user_token_email)
        user_num = cursor.fetchone()['user_num']
        cursor.execute("SELECT name FROM users WHERE email=%s", decode_user_token_email)
        user_name = cursor.fetchone()['name']
        cursor.execute("SELECT nickname FROM users WHERE email=%s", decode_user_token_email)
        user_nickname = cursor.fetchone()['nickname']
        cursor.execute("SELECT profile_text FROM users WHERE email=%s", decode_user_token_email)
        user_profile = cursor.fetchone()['profile_text']
        cursor.execute("SELECT created_at FROM users WHERE email=%s", decode_user_token_email)
        user_created_at = cursor.fetchone()['created_at']

        cursor.execute("SELECT profile_image_name FROM users WHERE email=%s", decode_user_token_email)
        # profile_image = cursor.fetchone()['profile_image_name']
        cache_cracker = datetime.datetime.utcnow()
        cursor.execute('SELECT user_num FROM users WHERE email=%s', decode_user_token_email)
        user_primary_key = cursor.fetchone()['user_num']
        cursor.execute('SELECT nickname FROM users WHERE email=%s', decode_user_token_email)
        user_nickname = cursor.fetchone()['nickname']
        user_link_primary = str(user_primary_key)+user_nickname
        profile_image_link = f'https://flask-user-image-storage.s3.ap-northeast-2.amazonaws.com/images/{user_link_primary}.jpg?{cache_cracker}'

        # create user_data dict
        user_data = {'user_link_primary' : user_link_primary , 'user_name' : user_name, 'user_nickname' : user_nickname,'user_profile' : user_profile, 'user_created_at' : user_created_at, 'user_profile_image_link' : profile_image_link}
        
        route_name = request.args.get("name", user_name)
        
        # checkout password
        if request.method == 'POST' and 'password' in request.form :
            password = str(request.form['password'])
            
            cursor.execute("SELECT password FROM users WHERE email=%s", decode_user_token_email)
            match_pwd = cursor.fetchone()
            check_password = bcrypt.checkpw(password.encode('utf-8'), match_pwd['password'])

            # if password same
            if(check_password == True) :
                flash('Comnfirmed password!')
                register_db.close()
                
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
                    register_db.close()

                    return redirect(url_for('flask_user.user'))
                else :
                    endcode_change_password = (bcrypt.hashpw(change_password.encode('UTF-8'), bcrypt.gensalt())).decode('utf-8')
                    cursor.execute("UPDATE users SET password=%s WHERE email=%s", (endcode_change_password, decode_user_token_email))
                    register_db.commit()
                    register_db.close()
    
                    flash('UserData Change Completed!')
                    return redirect(url_for('flask_user.user'))

        # if get POST change_nickname and change_profile
        if request.method == 'POST' and 'change_nickname' in request.form and 'change_profile' in request.form:
            print('hi')
            change_nickname = str(request.form['change_nickname'])
            change_profile = str(request.form['change_profile'])

            cursor.execute("UPDATE users SET nickname=%s WHERE email=%s", (change_nickname, decode_user_token_email))
            register_db.commit()
            
            cursor.execute("UPDATE users SET profile_text=%s WHERE email=%s", (change_profile, decode_user_token_email))
            register_db.commit()
            register_db.close()

            flash('UserData Change Completed!')
            return redirect(url_for('flask_user.user'))

        # if get POST delete_user
        if request.method == 'POST' and 'delete_user' in request.form :
            flash('Are you sure really delete your account?')
            register_db.close()

            return render_template(really_delete=True)

    else :
        register_db.close()
        
        return render_template("user.html", name = route_name, user_data = user_data, user_name = user_name)

