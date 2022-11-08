from flask import render_template, request, redirect, url_for, Blueprint
import pymysql

bp = Blueprint('update_post', __name__, url_prefix='/')

@bp.route('/update_post/<update_board_number>', methods=['GET','POST'])
def update_post(update_board_number):
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
        cursor.execute("SELECT title, content, category, max_team, start_day, contect, tech_stack FROM test WHERE board_num = '{}'".format(update_board_number))
        update_post = cursor.fetchall()
        return render_template('update_post.html', update_post=update_post)
    if request.method == "POST":
        update_title = request.form['update_title']
        update_content = request.form['update_content'] 
        update_category = request.form['update_category']
        update_max_team = request.form['update_max_team']
        update_start_day = request.form['update_start_day']
        update_contect = request.form['update_contect']
        update_tech_stack = request.form['update_tech_stack']
        cursor.execute("UPDATE board SET title = '{}', content = '{}', category = '{}', max_team = {}, start_day = '{}', contect = '{}', tech_stack = '{}' WHERE board_num = {}".format(update_title,update_content,update_category,update_max_team,update_start_day,update_contect,update_tech_stack,update_board_number))#update 코드
        db.commit()
        db.close()
        return redirect(url_for('showpost_list.showpost_list'))