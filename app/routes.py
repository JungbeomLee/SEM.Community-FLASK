from flask import redirect, url_for, render_template, request, Blueprint
from app.events import MyNamespace

roomname = MyNamespace()

main = Blueprint('main', __name__)


# @main.route('/', methods = ['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         session['roomname'] = request.form['room']
#         return redirect(url_for('main.chatting', room = session['roomname']))
#     return render_template('index.html')

@main.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        return redirect(url_for('main.chatting'))
    return render_template('index.html')

@main.route('/chat')
def chatting():
    return render_template('chat.html', roomname = roomname.on_join)    

# @main.route('/chat/<room>')
# def chatting(room):
#     if room == session['roomname'] : 
#         return render_template('chat.html', room = session['roomname'])
#     else :
#         print('Room is None')
#         result = '등록된 방 이름이 아닙니다.'
#         return result