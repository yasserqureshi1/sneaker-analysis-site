from flask import Blueprint, request, render_template
from app import stockx, marketplaces, twitter
from .models import Brands, db
from datetime import datetime
import json


view = Blueprint("view", __name__)
api = twitter.authentication()


def search():
    shoe_name = request.form['search']
    if shoe_name != '':
        names = stockx.find_item(shoe_name)
        return render_template('search.html', results=names)
    else:
        return render_template('search.html')


@view.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #search()
        shoe_name = request.form['search']
        if shoe_name != '':
            names = stockx.find_item(shoe_name)
            return render_template('search.html', results=names)

    return render_template('index.html')


@view.route('/shoe', methods=['GET', 'POST'])
def shoe():
    if request.method == 'POST':
        search()
    return render_template('shoe.html')


@view.route('/shoe/<item>', methods=['GET', 'POST'])
def product_item(item):
    if request.method == 'POST':
        search()

    # Product Details from Stockx
    data = stockx.get_product_details(item)
    
    # Product price plots
    raw_series = stockx.get_datapoints(item)
    labels = [str(datetime.fromtimestamp(i[0]/1000)) for i in raw_series]
    values = [i[1] for i in raw_series]

    # Twitter top 100
    tweets = twitter.last_100_tweets(api, data['brand'])

    return render_template('shoe.html', data=data, labels=json.dumps(labels), values=json.dumps(values), tweets=tweets)


@view.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        search()
    
    return render_template('about.html')


@view.route('/brands', methods=['GET', 'POST'])
def brands():
    if request.method == 'POST':
        search()

        if 'alpha' in request.form:
            brands = Brands.query.filter(Brands.name.startswith(request.form['alpha'].upper())).order_by(Brands.name).all()

    else:
        brands = Brands.query.all()
    
    return render_template('brands.html', brands=brands)


@view.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method =='POST':
        search()
    return render_template('contact.html')

    