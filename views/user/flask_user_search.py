from flask import Blueprint, render_template, request, url_for, redirect
from ..utils.env_var import database_pwd
import pymysql

bp = Blueprint('flask_user_search', __name__, url_prefix='/')

@bp.route('/user/other_user', methods=['GET','POST'])
def user_search() :
    # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "sebuung_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)

    # select all user_nickname
    cursor.execute("SELECT nickname FROM users")
    search_user_nickname = cursor.fetchall()
    search_result = True

    # save all user_nickname to list
    search_user_nickname_list = []
    for i in range(len(search_user_nickname)) :
        search_user_nickname_list.append(search_user_nickname[i]['nickname'])
    
    # get url parameters
    search_nickname = request.args.get('search')
    # checkout url parameters
    if search_nickname :
        # search for similar user_nickname in database
        cursor.execute('SELECT nickname FROM users WHERE nickname like "%{}%"'.format(search_nickname))
        search_user_nickname = cursor.fetchall()
        register_db.close()
        
        # check search result
        if search_user_nickname :
            search_result = True
            search_user_nickname_list = []

            # make search results to list
            for i in range(len(search_user_nickname)) :
                search_user_nickname_list.append(search_user_nickname[i]['nickname'])
        else :
            search_result = False

    # return form parameters to url parameters
    if request.method == 'POST' and 'search_user_nickname' in request.form :
        # get POST form_search_nickname
        form_search_nickname = request.form['search_user_nickname']
        register_db.close()

        return redirect(url_for('flask_user_search.user_search', search = form_search_nickname))
    
    return render_template('user_search.html', search_user_nickname_list = search_user_nickname_list, search_result = search_result)
