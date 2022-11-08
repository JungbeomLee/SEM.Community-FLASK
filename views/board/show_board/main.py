from flask import render_template, Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')