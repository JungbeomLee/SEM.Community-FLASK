from flask import Flask, render_template, request, redirect, url_for, Blueprint
import pymysql

bp = Blueprint('showpost_list', __name__, url_prefix='/')

@bp.route('/showpost_list', methods=['GET','POST'])
def showpost_list():
    # board db connect
    db = pymysql.connect(
        user='root',
        passwd='0000',
        host='localhost',
        port=3306,
        db='sebuung_db',
        charset='utf8'
    )
    cursor = db.cursor()

    cursor.execute("SELECT board_num, title, category, start_day, tech_stack FROM test")
    post_list = cursor.fetchall()
    db.close()
    return render_template('showpost_list.html', post_list=post_list)