from flask import request, redirect, url_for, Blueprint
import pymysql

bp = Blueprint('posting', __name__, url_prefix='/')

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
            cursor.execute(
                "INSERT INTO test(title,content,category,max_team,start_day,contect,tech_stack) VALUES('{0}','{1}','{2}',{3},'{4}','{5}','{6}');"
                .format(title,content,category,max_team,start_day,contect,tech_stack))    
            db.commit()
            db.close()
        except:
            return redirect(url_for('main'))
    return redirect(url_for('main'))