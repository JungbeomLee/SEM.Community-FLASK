from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()

def create_app() : 
    flask_secret_key = os.environ.get('FLASK_KEY')
    app = Flask(__name__)
    app.secret_key = flask_secret_key
    app.config['JSON_AS_ASCII'] = False

    from views import flask_token, flask_main
    from views.sign_up import flask_login, flask_register, flask_logout
    from views.user import flask_delete_account, flask_user_change_pwd, flask_other_user, flask_user_search
    from views.user import flask_own_user
    from views.board.operate_board import posting, delete_post, update_post
    from views.board.show_board import write_board, showpost_list, showpost
    
    app.register_blueprint(flask_main.bp)
    app.register_blueprint(flask_register.bp)
    app.register_blueprint(flask_login.bp)
    app.register_blueprint(flask_token.bp)
    app.register_blueprint(flask_own_user.bp)
    app.register_blueprint(flask_delete_account.bp)
    app.register_blueprint(flask_user_change_pwd.bp)
    app.register_blueprint(flask_logout.bp)
    app.register_blueprint(flask_other_user.bp)
    app.register_blueprint(flask_user_search.bp)
    app.register_blueprint(posting.bp)
    app.register_blueprint(write_board.bp)
    app.register_blueprint(showpost_list.bp)
    app.register_blueprint(showpost.bp)
    app.register_blueprint(delete_post.bp)
    app.register_blueprint(update_post.bp)

    app.run(host='0.0.0.0', port=8000, debug=True)

create_app()