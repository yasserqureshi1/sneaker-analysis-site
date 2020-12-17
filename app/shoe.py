from flask import Blueprint
from flask import render_template
from app import StockXscraper

shoe = Blueprint("shoe", __name__)


@shoe.route('/shoe/<item>')
def product_item(item):
    data = StockXscraper.getProductDetails(item)
    labels = [1,2,3,4,5]
    values = [1,2,3,4,5]
    return render_template('shoe.html', data=data, labels=labels, values=values)

