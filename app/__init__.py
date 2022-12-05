from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(engineio_logger=True, logger=True)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    socketio.init_app(app)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.events import socketio_init
    socketio_init(socketio)

    return app
