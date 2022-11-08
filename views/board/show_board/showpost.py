from flask import render_template, request, Blueprint
import pymysql

bp = Blueprint('posting', __name__, url_prefix='/')

@bp.route('/post/<select_board_number>', methods=['GET', 'POST'])
def showpost(select_board_number):
    db = pymysql.connect(
        user='root',
        passwd='0000',
        host='localhost',
        port=3306,
        db='sebuung_db',
        charset='utf8'
    )
    cursor = db.cursor()

    if request.method == "GET": 
        cursor.execute("SELECT * FROM test WHERE board_num = '{}'".format(select_board_number))
        post_content = cursor.fetchall()
        db.close()
    return render_template('showpost.html', post_content = post_content)