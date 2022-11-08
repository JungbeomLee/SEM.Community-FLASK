from flask import Blueprint, render_template
from ...utils.check_token import CHECK_TOKEN
from dotenv import load_dotenv

load_dotenv('../env')

bp = Blueprint('flask_user', __name__, url_prefix='/user')

@bp.route('/own_user')
@CHECK_TOKEN.check_for_token
def user() :
    
    return render_template("user.html")