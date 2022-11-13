from flask import Blueprint, render_template, request, flash, session
from views.utils.check_token import CHECK_TOKEN
from views.utils.env_var import database_pwd
from views.utils.upload_image_to_s3 import s3_put_object
from views.utils.connect_aws import s3_connection
import pymysql

bp = Blueprint('flask_own_user_upload_image_post', __name__, url_prefix='/user/own_user/upload_image')

@bp.route('post', methods=['POST'])
@CHECK_TOKEN.check_for_token
def user_profile_upload_image() :
    if request.method =='POST' :
        reps = {'posting_image' : True}
        
        reqeust_user_upload_image_file = request.files['upload_user_image']

        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "sebuung_db", 
            charset="utf8"
        )
        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        cursor.execute('SELECT user_num FROM users WHERE email=%s', session['user_email'])
        user_primary_key = cursor.fetchone()['user_num']
        cursor.execute('SELECT nickname FROM users WHERE email=%s', session['user_email'])
        user_nickname = cursor.fetchone()['nickname']

        profile_image_name = str(user_primary_key)+user_nickname

        s3 = s3_connection()
        check_image_upload_s3 = s3_put_object(s3, reqeust_user_upload_image_file, profile_image_name)

        reps['check_image_upload_s3'] = check_image_upload_s3

        cursor = register_db.cursor(pymysql.cursors.DictCursor)

        if check_image_upload_s3 == True :
            own_user_email = session['user_email']

            cursor.execute('UPDATE users SET profile_image_name=%s WHERE email=%s', (profile_image_name, own_user_email))
            register_db.commit()
            register_db.close()

            return reps
        else :
            reps = {'posting_image' : False}

            return reps