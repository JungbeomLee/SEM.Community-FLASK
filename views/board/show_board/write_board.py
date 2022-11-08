from flask import render_template, Blueprint

bp = Blueprint('write_board', __name__, url_prefix='/')

@bp.route('/write_board')
def write_board():
    return render_template('write_board.html')