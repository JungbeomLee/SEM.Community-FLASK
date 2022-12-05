from flask import request, redirect, url_for, Blueprint, session
from ...utils.env_var import database_pwd, jwt_secret_key
import pymysql
import jwt

bp = Blueprint('post_writed', __name__, url_prefix='/')

@bp.route('/posting', methods=['GET','POST'])
def posting():  
    # board db connect
    db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        port=3306,
        db=     "sebuung_db", 
        charset="utf8"
    )

    cursor_board = db.cursor()

    #Markdown 구현 https://wikidocs.net/81066

    if request.method == "POST":
        access_token = request.cookies.get('access_token')
        decode_access_token_emil = jwt.decode(access_token, jwt_secret_key, algorithms='HS256')['user_email']
        # connect mysql database
        register_db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "sebuung_db", 
            charset="utf8"
        )
        cursor_user = register_db.cursor(pymysql.cursors.DictCursor)

        # create user_data dict variable
        # get user_data
        cursor_user.execute("SELECT nickname FROM users WHERE email=%s", decode_access_token_emil)
        user_nickname = cursor_user.fetchone()['nickname']

        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        max_team = request.form['max_team']
        start_day = request.form['start_day']
        contect = request.form['contect']
        tech_stack = request.form['tech_stack']

        cursor_board.execute(
            "INSERT INTO board(title,content,category,max_team,start_day,contect,tech_stack, writer_nickname, writer_email) VALUES('{0}','{1}','{2}',{3},'{4}','{5}','{6}','{7}','{8}');"
            .format(title,content,category,max_team,start_day,contect,tech_stack,user_nickname,decode_access_token_emil))    
        db.commit()
        db.close()
    return redirect(url_for('showpost_list.showpost_list'))