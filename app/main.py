from flask import Blueprint, request, redirect, url_for
from flask import render_template
from app import StockXscraper


home = Blueprint("home", __name__)


@home.route('/')
def home_page():
    return render_template('home.html')


@home.route('/', methods=['POST'])
def search():
    shoe_name = request.form['sneaker']
    names = StockXscraper.findItem(shoe_name)
    return render_template('selection.html', results=names)

