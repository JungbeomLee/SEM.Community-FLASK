from flask import request, redirect, url_for, Blueprint
from views.utils.check_token import CHECK_TOKEN
from ...utils.env_var import database_pwd
import pymysql

bp = Blueprint('delete_post', __name__, url_prefix='/')
#@CHECK_TOKEN
@bp.route('/delete_post/<delete_board_number>', methods=['GET', 'POST'])
def delete_post(delete_board_number):
    db = pymysql.connect(
        user='root',
        passwd=database_pwd,
        host='localhost',
        port=3306,
        db='sebuung_db',
        charset='utf8'
    )
    cursor = db.cursor()

    if request.method == "GET":
        cursor.execute("DELETE FROM board WHERE board_num = '{}'".format(delete_board_number))
        db.commit()
        db.close()
    return redirect(url_for('showpost_list.showpost_list'))