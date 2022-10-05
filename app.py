from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

flask_secret_key = os.environ.get('FLASK_KEY')

def create_app() : 
    app = Flask(__name__)
    app.secret_key = flask_secret_key
    
    from views import flask_main_views
    app.register_blueprint(flask_main_views.bp)

    from views.sign_up import flask_login, flask_register, flask_user
    app.register_blueprint(flask_register.bp)
    app.register_blueprint(flask_login.bp)
    app.register_blueprint(flask_user.bp)

    if __name__ == "__main__" : 
        app.run(host='0.0.0.0', port=8000, debug=True)

create_app()