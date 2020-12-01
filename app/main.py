from flask import Blueprint
from flask import render_template


home = Blueprint("home", __name__)


@home.route('/')
def home_page():
    return render_template('home.html')
