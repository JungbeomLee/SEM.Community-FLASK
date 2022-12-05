from flask import session
from flask_socketio import emit, join_room, leave_room

def socketio_init(socketio):
    @socketio.event
    def join(message):
        room_name = message['room_name']
        join_room(session.get(room_name))
        emit('my_response',
             {'data': message['data']}, room=session.get(room_name))

    @socketio.event
    def message(message):
        room_name = message['room_name']
        print(message['data'])
        emit('my_response',
             {'data': message['data']}, room=session.get(room_name))

    # @socketio.event
    # def leave(message):
    #     leave_room(message['room_name'])
    #     emit('my_response',
    #          {'data': 'In rooms: ' + session.get(message['room_name'])})

