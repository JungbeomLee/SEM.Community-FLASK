from flask import render_template, Blueprint, request
from views.utils.check_token import CHECK_TOKEN

bp = Blueprint('write_board', __name__, url_prefix='/')
@bp.route('/write_board')
@CHECK_TOKEN.check_for_token
def write_board():
        return render_template('write_board.html')