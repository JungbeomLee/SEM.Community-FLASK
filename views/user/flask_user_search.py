from flask import Blueprint, render_template, request, flash, url_for, redirect
from dotenv import load_dotenv
from ..utils.env_var import database_pwd
import pymysql

load_dotenv('../env')

bp = Blueprint('flask_user_search', __name__, url_prefix='/')

@bp.route('/user', methods=['GET','POST'])
def user_search() :
    # connect mysql database
    register_db = pymysql.connect(
        host=   "localhost",
        user=   "root", 
        passwd= database_pwd, 
        db=     "register_db", 
        charset="utf8"
    )
    cursor = register_db.cursor(pymysql.cursors.DictCursor)

    # select all user_name
    cursor.execute("SELECT name FROM users")
    search_user_name = cursor.fetchall()

    # save all user_name to list
    search_user_name_list = []
    for i in range(len(search_user_name)) :
        search_user_name_list.append(search_user_name[i]['name'])
    
    if request.method == 'POST' and 'search_user_name' in request.form :
        search_name = request.form['search_user_name']

        cursor.execute('SELECT name FROM users WHERE name like "%{}%"'.format(search_name))
        search_user_name = cursor.fetchall()
        search_user_name_list = []

        for i in range(len(search_user_name)) :
            search_user_name_list.append(search_user_name[i]['name'])

        return render_template('user_search.html', search_user_name = search_user_name_list)
    
    return render_template('user_search.html', search_user_name = search_user_name_list)
