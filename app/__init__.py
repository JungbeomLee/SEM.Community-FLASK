from flask import Flask
from flask_socketio import SocketIO

socket_io = SocketIO(logger=True, engineio_logger=True)


def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'

    socket_io.init_app(app)

    from app.events import MyNamespace
    socket_io.on_namespace(MyNamespace('/'))

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    
    return app