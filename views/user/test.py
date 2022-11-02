from flask import Blueprint, request, redirect, url_for
from dotenv import load_dotenv
load_dotenv('../env')

bp = Blueprint('flask_user_test', __name__, url_prefix='/')

@bp.route('/user/test', methods=['GET','POST'])
def index(): 
    return redirect(url_for('flask_user_test.profile', username="hong"))

@bp.route('/user/test/test')
def profile(): 
    username = request.args.get('username')
    return username
