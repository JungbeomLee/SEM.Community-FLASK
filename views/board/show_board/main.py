from flask import Flask, render_template, request, redirect, url_for, Blueprint
import pymysql

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main.html')