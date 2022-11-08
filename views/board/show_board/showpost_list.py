from flask import render_template, Blueprint
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

#검색 기능 구현하기
@bp.route('/showpost_list/<search_word>', methods=['GET', 'POST'])
def search(search_word):
    db = pymysql.connect(
        user='root',
        passwd='0000',
        host='localhost',
        port=3306,
        db='sebuung_db',
        charset='utf8'
    )
    cursor = db.cursor()

    search_word = request.form['search_word']
    cursor.execute("SELECT board_num, title, category, start_day, tech_stack FROM test WHERE title LIKE '%{}%'".format(search_word))
    search_post_list = cursor.fetchall()
    db.close()
    return render_template('showpost_list.html', search_post_list=search_post_list)
