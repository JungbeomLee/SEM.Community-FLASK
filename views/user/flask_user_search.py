from flask import Blueprint, render_template, request, url_for, redirect
from ..utils.env_var import database_pwd
import pymysql

bp = Blueprint('flask_user_search', __name__, url_prefix='/')

@bp.route('/user', methods=['GET','POST'])
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

    # select all user_name
    cursor.execute("SELECT name FROM users")
    search_user_name = cursor.fetchall()
    search_result = True

    # save all user_name to list
    search_user_name_list = []
    for i in range(len(search_user_name)) :
        search_user_name_list.append(search_user_name[i]['name'])
    
    # get url parameters
    search_name = request.args.get('search')
    # checkout url parameters
    if search_name :
        # search for similar user_name in database
        cursor.execute('SELECT name FROM users WHERE name like "%{}%"'.format(search_name))
        search_user_name = cursor.fetchall()
        register_db.close()
        
        # check search result
        if search_user_name :
            search_result = True
            search_user_name_list = []

            # make search results to list
            for i in range(len(search_user_name)) :
                search_user_name_list.append(search_user_name[i]['name'])
        else :
            search_result = False

    # return form parameters to url parameters
    if request.method == 'POST' and 'search_user_name' in request.form :
        # get POST form_search_name
        form_search_name = request.form['search_user_name']
        register_db.close()

        return redirect(url_for('flask_user_search.user_search', search = form_search_name))
    
    return render_template('user_search.html', search_user_name_list = search_user_name_list, search_result = search_result)
