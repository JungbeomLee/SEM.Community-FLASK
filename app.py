from flask import Flask
import os

def create_app() : 
    flask_secret_key = os.environ.get('FLASK_KEY')
    app = Flask(__name__)
    app.secret_key = flask_secret_key
    app.config['JSON_AS_ASCII'] = False

    from views.sign_up import flask_register
    from views.sign_up.post import flask_register_post, flask_register_nickname_check
    from views import flask_main
    from views.sign_up import flask_login, flask_logout
    from views.user import flask_delete_account, flask_user_change_pwd, flask_other_user, flask_user_search
    from views.user.own_user import flask_own_user, flask_own_user_upload_image
    from views.user.own_user.post import flask_own_user_password_post, flask_own_change_user_data_post, flask_own_user_image_post, flask_own_user_nickname_check
    from views.user.own_user.get import flask_own_user_get
    from views.board.operate_board import posting, delete_post, update_post
    from views.board.show_board import write_board, showpost_list, showpost
    
    app.register_blueprint(flask_main.bp)
    app.register_blueprint(flask_register.bp)
    app.register_blueprint(flask_register_post.bp)
    app.register_blueprint(flask_register_nickname_check.bp)
    app.register_blueprint(flask_login.bp)
    app.register_blueprint(flask_own_user.bp)
    app.register_blueprint(flask_own_user_get.bp)
    app.register_blueprint(flask_own_user_password_post.bp)
    app.register_blueprint(flask_own_change_user_data_post.bp)
    app.register_blueprint(flask_own_user_upload_image.bp)
    app.register_blueprint(flask_own_user_image_post.bp)
    app.register_blueprint(flask_own_user_nickname_check.bp)
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