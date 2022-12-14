from flask import Blueprint, render_template, make_response, request, session
from urllib import parse
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
    first_meet_cookie_content =  parse.quote('hi this is when we meet first time!. Maybe...'+str(datetime.datetime.utcnow()))
    first_meet.set_cookie('first_meet', first_meet_cookie_content)
    return first_meet

  access_token = request.cookies.get('access_token')

  if access_token :
    login_status = True
    
  return render_template('index.html', login_status = login_status)