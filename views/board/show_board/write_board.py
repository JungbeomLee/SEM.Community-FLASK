from flask import Flask, render_template, request, redirect, url_for, Blueprint
import pymysql

bp = Blueprint('write_board', __name__, url_prefix='/')

@bp.route('/write_board')
def write_board():
    return render_template('write_board.html')