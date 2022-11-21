from flask import Blueprint, request
import pymysql
from ...utils.env_var import database_pwd


bp = Blueprint('flask_register_nickname_check', __name__, url_prefix='/register')

@bp.route('/registerchecknickname', methods=['POST'])
def register_post() :
  # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "sebuung_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)
    # --------------------------------------------------------------------------------------------------------------
    # nickname duplicate check
    if request.method == 'POST' and 'user_nickname' in request.form :
        request_nickname = request.form['user_nickname'].lower()
        
        try : 
            cursor.execute("SELECT nickname FROM users WHERE nickname=%s", request_nickname)
            db_nickname = cursor.fetchone()['nickname'].lower()
        except :
            db_nickname = ''

        if request_nickname != db_nickname :
            reps = {'nickname_duplicate_check' : 1}
        else :
            reps = {'nickname_duplicate_check' : -1}

        return reps
        