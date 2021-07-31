from flask import Blueprint, request, render_template, flash
from app import stockx, marketplaces, twitter, goat
from datetime import datetime
import statistics
import json

view = Blueprint("view", __name__)
api = twitter.authentication()


@view.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@view.route('/shoe', methods=['GET', 'POST'])
def shoe():
    return render_template('shoe.html')


@view.route('/shoe/<item>', methods=['GET', 'POST'])
def product_item(item):
    try:
        # Product Details from Stockx
        data = stockx.get_product_details(item)
        
        # Product price plots
        raw_series = stockx.get_datapoints(item)
        labels = [(datetime.fromtimestamp(i[0]/1000)) for i in raw_series]
        labels = [f'{label.month} - {label.year}' for label in labels]
        values = [i[1] for i in raw_series]

        # Twitter top 100
        tweets = twitter.last_100_tweets(api, data['brand'])
    except Exception as e:
        print(e)
        return render_template('errors/mistakes.html')

    # StockX stats
    stats = stockx.get_prices(item)
    try:
        _stockx = {
            'lowest_ask': stats['lowestAsk'],
            'average_price': stats['averageDeadstockPrice'],
            'highest_bid': stats['highestBid']
        }
    except Exception as e:
        print(e)
        _stockx = {}

    # GOAT stats
    stats = marketplaces.GOATPriceChecker(data['title']).scrape_site()
    try:
        _goat = {
            'lowest_price_gbp': stats['lowest_price_cents_gbp']/100,
            'lowest_price_usd': stats['lowest_price_cents']/100
        }
    except Exception as e:
        print(e)
        _goat = {}

    # eBay stats
    stats = marketplaces.EbayPriceChecker(data['title']).get_current_prices()
    try:
        ebay = {
            'max': int(max(stats)),
            'min': int(min(stats)),
            'mean': int(statistics.mean(stats))
        }
    except Exception as e:
        print(e)
        ebay = {}

    # Depop stats
    stats = marketplaces.DepopPriceChecker(data['title']).get_current_prices()
    try:
        depop = {
            'max': int(max(stats)),
            'min': int(min(stats)),
            'mean': int(statistics.mean(stats))
        }
    except Exception as e:
        print(e)
        depop = {}

    return render_template('shoe.html', 
        data=data, 
        labels=json.dumps(labels), 
        values=json.dumps(values), 
        tweets=tweets, 
        ebay=ebay, 
        depop=depop,
        stockx=_stockx,
        goat=_goat
    )


@view.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')



@view.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


@view.route('/search', methods=['POST', 'GET'])
def search():
    shoe_name = request.form['search']
    if shoe_name != '':
        names = stockx.find_item(shoe_name)
        return render_template('search.html', results=names)
    flash('No Results')
    return render_template('search.html')
    