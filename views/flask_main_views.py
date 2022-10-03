from flask import Blueprint, render_template

bp = Blueprint('main', __name__, url_prefix='/')

# custom error page
@bp.app_errorhandler(404)
def not_found_error(error):
  return render_template('page404.html'), 404

# main page
@bp.route('/')
def main_page() :
  return render_template('index.html')