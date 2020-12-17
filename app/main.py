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
    if shoe_name != '':
        names = StockXscraper.findItem(shoe_name)
        return render_template('selection.html', results=names)


@home.route('/<any>', methods=['POST'])
def search_any(any):
    shoe_name = request.form['sneaker']
    if shoe_name != '':
        names = StockXscraper.findItem(shoe_name)
        return render_template('selection.html', results=names)


@home.route('/shoe/<any>', methods=['POST'])
def search_shoe(any):
    shoe_name = request.form['sneaker']
    if shoe_name != '':
        names = StockXscraper.findItem(shoe_name)
        return render_template('selection.html', results=names)


@home.route('/<random>')
def not_found_page(random):
    return render_template('not_found.html', page=random)