from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app() : 
    flask_secret_key = os.environ.get('FLASK_KEY')
    app = Flask(__name__)
    app.secret_key = flask_secret_key
    app.config['JSON_AS_ASCII'] = False
    
    from views import flask_main_views
    app.register_blueprint(flask_main_views.bp)

    from views import flask_token, flask_user
    from views.sign_up import flask_login, flask_register
    app.register_blueprint(flask_register.bp)
    app.register_blueprint(flask_login.bp)
    app.register_blueprint(flask_token.bp)
    app.register_blueprint(flask_user.bp)

    app.run(host='0.0.0.0', port=8000, debug=True)

create_app()