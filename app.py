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

    from views import flask_token
    from views.sign_up import flask_login, flask_register, flask_logout
    from views.user import flask_delete_account, flask_user_change_pwd, flask_other_user, flask_user_search
    from views.user.own_user import flask_own_user, flask_own_user_upload_image, flask_own_user_get, flask_own_user_post

    app.register_blueprint(flask_register.bp)
    app.register_blueprint(flask_login.bp)
    app.register_blueprint(flask_token.bp)
    app.register_blueprint(flask_own_user.bp)
    app.register_blueprint(flask_delete_account.bp)
    app.register_blueprint(flask_user_change_pwd.bp)
    app.register_blueprint(flask_logout.bp)
    app.register_blueprint(flask_other_user.bp)
    app.register_blueprint(flask_user_search.bp)
    app.register_blueprint(flask_own_user_upload_image.bp)
    app.register_blueprint(flask_own_user_get.bp)
    app.register_blueprint(flask_own_user_post.bp)

    app.run(host='0.0.0.0', port=8000, debug=True)

create_app()