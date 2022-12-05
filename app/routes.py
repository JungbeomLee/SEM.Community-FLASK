from flask import Blueprint, render_template, request, url_for, redirect, session
import pymysql
import db_config
import sys

main = Blueprint('main', __name__)

rds_host = "localhost"
name = db_config.db_username
password = db_config.db_password
db_name = db_config.db_name

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name)
except pymysql.MySQLError as e:
    print("ERROR: Unexpected error: Could not connect to MySQL instance.")
    print(e)
    sys.exit()


@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(list(session))
        return render_template('index.html', room_name=list(session))
    return render_template('index.html', room_name=list(session))


@main.route('/create', methods=['GET', 'POST'])
def create_room():
    if request.method == 'POST':
        room_name = request.form['room_name']
        with conn.cursor() as cur:
            cur.execute('SELECT room_title FROM room_table WHERE room_title LIKE "{0}"'.format(room_name))
            result = cur.fetchall()
            if not result:
                cur.execute('INSERT INTO room_table(room_title) values ("{0}")'.format(room_name))
                conn.commit()
                if room_name != '':
                    session[room_name + ' Room'] = room_name
                print("Success Add Room")
        return redirect(url_for('main.room_name', room_name=room_name + ' Room'))
    return render_template('create.html')


@main.route('/room/<room_name>', methods=['GET', 'POST'])
def room_name(room_name):
    print(room_name)
    return render_template('chatting.html', room_name=room_name)


@main.route('/clear', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        room_name = request.form['room_name']
        with conn.cursor() as cur:
            sql1 = 'DELETE FROM room_table WHERE room_title = "{0}"'.format(room_name)
            sql2 = 'UPDATE `room_table` SET room_id = @COUNT:=@COUNT+1'
            sql3 = 'ALTER TABLE room_table AUTO_INCREMENT=1'
            cur.execute('SET @COUNT = 0')
            cur.execute(sql1)
            cur.execute(sql2)
            cur.execute(sql3)
            conn.commit()
            session.pop(room_name + ' Room')
        return redirect(url_for('main.index'))
    return render_template('clear.html')
