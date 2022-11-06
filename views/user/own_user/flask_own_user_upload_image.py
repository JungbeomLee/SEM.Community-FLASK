from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from ...utils.check_token import CHECK_TOKEN
from ...utils.env_var import database_pwd
from ...utils.upload_image_to_s3 import s3_put_object
from ...utils.connect_aws import s3_connection
import pymysql

bp = Blueprint('flask_own_user_upload_image', __name__, url_prefix='/')

@bp.route('/user/own_user/upload_image', methods=['GET','POST'])
@CHECK_TOKEN.check_for_token
def user_profile_upload_image() :
    check_image_upload_html = False
    if request.method =='POST' :
        reqeust_user_upload_image_file = request.files['upload_user_image']
        
        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "register_db", 
            charset="utf8"
        )
        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        cursor.execute('SELECT user_num FROM users WHERE email=%s', session['user_email'])
        user_primary_key = cursor.fetchone()['user_num']
        cursor.execute('SELECT nickname FROM users WHERE email=%s', session['user_email'])
        user_nickname = cursor.fetchone()['nickname']

        s3 = s3_connection()
        check_image_upload = s3_put_object(s3, reqeust_user_upload_image_file, str(user_primary_key)+user_nickname)
        
        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "register_db", 
            charset="utf8"
        )
        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        cursor.execute('SELECT user_num FROM users WHERE email=%s', session['user_email'])
        user_primary_key = str(cursor.fetchone()['user_num'])
        cursor.execute('SELECT nickname FROM users WHERE email=%s', session['user_email'])
        user_nickname = cursor.fetchone()['nickname']
        profile_image_name = user_primary_key+user_nickname

        if check_image_upload == True :
            cursor.execute('UPDATE users SET profile_image_name=%s WHERE email=%s', (profile_image_name, session['user_email']))
            register_db.commit()
            register_db.close()
            
            flash('Successfully upload profile image')
            check_image_upload_html = True

            return render_template("upload_user_image.html", check_image_upload_html = check_image_upload_html)
        else :
            flash('Failed upload profile image')
            return render_template("upload_user_image.html", check_image_upload_html = check_image_upload_html)

    
    return render_template("upload_user_image.html", check_image_upload_html = check_image_upload_html)
