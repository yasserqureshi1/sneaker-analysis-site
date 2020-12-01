from flask import Blueprint
from flask import render_template


shoe = Blueprint("shoe", __name__)


@shoe.route('/shoe')
def shoe_page():
    return render_template('shoe.html')
