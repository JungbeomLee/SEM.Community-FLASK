from flask import Blueprint, render_template

bp = Blueprint('flask_register', __name__, url_prefix='/')

# my NEW register page
@bp.route('/register')
def register() :

  return render_template('register.html')