from flask import Blueprint, render_template, request
from ..utils.env_var import database_pwd
import pymysql
import datetime

bp = Blueprint('flask_other_user', __name__, url_prefix='/user/other_user')

@bp.route('/<route_user_nickname>', methods=['GET'])
def other_user(route_user_nickname) :
    # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "sebuung_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)

    # 입력받은 route_user_nickname이 실제 가입 유저인지 확인
    cursor.execute("SELECT nickname FROM users WHERE nickname=%s", route_user_nickname)

    check_route_user_nickname = cursor.fetchone()['nickname']

    if check_route_user_nickname :
        cursor.execute("SELECT email FROM users WHERE nickname=%s", route_user_nickname)
        route_search_user_email = cursor.fetchone()['email']

        # create user_data dict variable
        # get user_data
        cursor.execute("SELECT profile_image_name FROM users WHERE email=%s", route_search_user_email)
        other_user_profile_image_name = cursor.fetchone()['profile_image_name']
        cache_cracker = datetime.datetime.utcnow()
        profile_image_link = f'https://flask-user-image-storage.s3.ap-northeast-2.amazonaws.com/images/{other_user_profile_image_name}.jpg?{cache_cracker}'

        cursor.execute("SELECT name FROM users WHERE email=%s", route_search_user_email)
        other_user_name = cursor.fetchone()['name']
        
        cursor.execute("SELECT nickname FROM users WHERE email=%s", route_search_user_email)
        other_user_nickname = cursor.fetchone()['nickname']
        
        cursor.execute("SELECT profile_text FROM users WHERE email=%s", route_search_user_email)
        user_profile = cursor.fetchone()['profile_text']
        
        cursor.execute("SELECT created_at FROM users WHERE email=%s", route_search_user_email)
        user_created_at = cursor.fetchone()['created_at']
        register_db.close()

        # get user posting
        # board db connect
        db = pymysql.connect(
            host=   "localhost",
            user=   "root", 
            passwd= database_pwd, 
            db=     "sebuung_db", 
            charset="utf8"
        )
        cursor_board = db.cursor(pymysql.cursors.DictCursor)
        cursor_board.execute('SELECT board_num, title, writer_nickname, create_day, tech_stack  FROM board WHERE writer_email=%s',route_search_user_email)
        other_user_posting = cursor_board.fetchall()
        
        other_user_posting_list = []
        for i in range(len(other_user_posting)) :
            other_user_posting_dict = {
                "board_num" : other_user_posting[i]['board_num'],
                "title" : other_user_posting[i]['title'],
                "writer_nickname" : other_user_posting[i]['writer_nickname'],
                "create_day" : other_user_posting[i]['create_day'],
                "tech_stack" : other_user_posting[i]['tech_stack']
            }
            other_user_posting_list.append(other_user_posting_dict)
        
        # create user_data dict
        data = {
            'profile_image_link' : profile_image_link, 
            'user_name' : other_user_name, 
            'other_user_nickname' : other_user_nickname, 
            'user_profile' : user_profile, 
            'user_created_at' : user_created_at,
            'other_user_posting_data' : other_user_posting_list
        }

        return render_template("other_user.html", data = data)        

