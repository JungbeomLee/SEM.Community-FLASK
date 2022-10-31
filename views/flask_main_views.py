from flask import Blueprint, render_template, make_response, request, session
from .utils.check_token import CHECK_TOKEN
import datetime

bp = Blueprint('flask_main', __name__, url_prefix='/')

# custom error page
@bp.app_errorhandler(404)
def not_found_error(error):
  return render_template('page404.html'), 404

# main page
@bp.route('/')
def main_page() :
  get_first_meet = request.cookies.get('first_meet')

  login_status = False

  if not get_first_meet : 
    first_meet = make_response(render_template('index.html'))
    first_meet.set_cookie('first_meet', 'hi this is when we meet first time!. Maybe...'+str(datetime.datetime.utcnow()))
    return first_meet

  if 'user_email' in session :
    login_status = True

  return render_template('index.html', login_status = login_status)