from flask import Blueprint
from flask import render_template
from app import StockXscraper

shoe = Blueprint("shoe", __name__)


@shoe.route('/<item>')
def product_item(item):
    data = StockXscraper.getProductDetails(item)
    return render_template('shoe.html', data=data)

