from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

db = pymysql.connect(
    user='root',
    passwd='0000',
    host='localhost',
    port=3306,
    db='sebuung_db',
    charset='utf8'
)

cursor = db.cursor()


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

@app.route('/write_board')
def write_board():
    return render_template('write_board.html')

@app.route('/posting', methods=['GET','POST'])
def posting():
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
        except:
            return redirect(url_for('main'))
    return redirect(url_for('main'))

# 게시글 목록판
@app.route('/showpost_list', methods=['GET','POST'])
def showpost_list():
    cursor.execute("SELECT board_num, title, category, start_day, tech_stack FROM test")
    post_list = cursor.fetchall()
    return render_template('showpost_list.html', post_list=post_list)

#게시글 내용 보기
@app.route('/post/<select_board_number>', methods=['GET', 'POST'])
def showpost(select_board_number):
    if request.method == "GET":
        cursor.execute("SELECT * FROM test WHERE board_num = '{}'".format(select_board_number))
        post_content = cursor.fetchall()
    return render_template('showpost.html', post_content = post_content)

#게시글 삭제
@app.route('/delete_post/<delete_board_number>', methods=['GET', 'POST'])
def delete_post(delete_board_number):
    if request.method == "GET":
        cursor.execute("DELETE FROM test WHERE board_num = '{}'".format(delete_board_number))
        db.commit()
    return redirect(url_for('showpost_list'))

#게시글 수정 https://blogger.pe.kr/899
@app.route('/update_post/<update_board_number>', methods=['GET','POST'])
def update_post(update_board_number):
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
        cursor.execute("UPDATE test SET title = '{}', content = '{}', category = '{}', max_team = {}, start_day = '{}', contect = '{}', tech_stack = '{}' WHERE board_num = {}".format(update_title,update_content,update_category,update_max_team,update_start_day,update_contect,update_tech_stack,update_board_number))#update 코드
        db.commit()
        return redirect(url_for('showpost_list'))

if __name__ == '__main__':
    app.run(debug=True)

#https://smcjaemin0820.tistory.com/entry/2-Flask-%EC%B0%8D%EB%A8%B9%ED%95%B4%EB%B3%B4%EA%B8%B0