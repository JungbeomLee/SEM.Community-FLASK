from flask import request, redirect, url_for, Blueprint, session
import pymysql

bp = Blueprint('post_writed', __name__, url_prefix='/')

@bp.route('/posting', methods=['GET','POST'])
def posting():  
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

    #Markdown 구현 https://wikidocs.net/81066

    if request.method == "POST":
        try:
            title = request.form['title']
            content = request.form['content']
            category = request.form['category']
            max_team = request.form['max_team']
            start_day = request.form['start_day']
            contect = request.form['contect']
            tech_stack = request.form['tech_stack']
            email = session['user_email']
            cursor.execute(
                "INSERT INTO board(title,content,category,max_team,start_day,contect,tech_stack,email) VALUES('{0}','{1}','{2}',{3},'{4}','{5}','{6}','{7}');"
                .format(title,content,category,max_team,start_day,contect,tech_stack,email))    
            db.commit()
            db.close()
        except:
            return redirect(url_for('flask_main.not_found_error'))
    return redirect(url_for('showpost_list.showpost_list'))