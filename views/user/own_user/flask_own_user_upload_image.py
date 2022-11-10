from flask import Blueprint, render_template
from ...utils.check_token import CHECK_TOKEN


bp = Blueprint('flask_own_user_upload_image', __name__, url_prefix='/')

@bp.route('/user/own_user/upload_image')
@CHECK_TOKEN.check_for_token
def user_profile_upload_image() :

    return render_template("upload_user_image.html")