import requests
from bs4 import BeautifulSoup
import statistics
import json


class EbayPriceChecker:
    def __init__(self, item):
        self.item = item

    def get_current_prices(self):
        current_listings = []
        try:
            url = f'https://www.ebay.co.uk/sch/i.html?_nkw={self.item.replace(" ", "+")}&_ipg=200'
            html = requests.get(url=url)
            soup = BeautifulSoup(html.text, 'html.parser')

            for product in soup.find_all('div', {'class': 's-item__wrapper clearfix'}):
                try:
                    price = product.find('span', {'class': 's-item__price'}).text
                    try:
                        current_listings.append(float(price.replace('£', '')))
                    except:
                        price = price.replace(' to', '').replace('£', '').split()
                        prices = [float(item) for item in price]
                        current_listings.append(statistics.mean(prices))
                except Exception:
                    pass
        except Exception as e:
            print(f'Error: {e}')
        return current_listings

    def get_sold_prices(self):
        sold_listings = []
        try:
            url = f'https://www.ebay.co.uk/sch/i.html?_nkw={self.item.replace(" ", "+")}&_ipg=200&rt=nc&LH_Sold=1'
            html = requests.get(url=url)
            soup = BeautifulSoup(html.text, 'html.parser')
            for product in soup.find_all('div', {'class': 's-item__wrapper clearfix'}):
                try:
                    price = product.find('span', {'class': 's-item__price'}).text
                    try:
                        sold_listings.append(float(price.replace('£', '')))
                    except:
                        price = price.replace(' to', '').replace('£', '')
                        price = price.split()
                        sold_listings.append(statistics.mean([float(item) for item in price]))
                except Exception:
                    pass
        except:
            print('Error occurred')
        return sold_listings


class DepopPriceChecker:
    def __init__(self, item):
        self.item = item

    def get_current_prices(self):
        current_listings = []
        try:
            url = f'https://webapi.depop.com/api/v2/search/products/?what={self.item.replace(" ", "%20")}&country=gb&itemsPerPage=200&currency=GBP'
            html = requests.get(url=url).text
            output = json.loads(html)
            for i in output['products']:
                price = i['price']['priceAmount']
                current_listings.append(float(price))
        except Exception as e:
            print(f'Error: {e}')
        return current_listings


class GOATPriceChecker:
    def __init__(self, item):
        self.item = item
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        self.params = {'x-algolia-agent': 'Algolia for vanilla JavaScript 3.25.1',
                       'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a',
                       'x-algolia-application-id': '2FWOTDVM2O'}
        self.data = {"params": "query={}&facetFilters=(status%3Aactive%2C%20status%3Aactive_edit)%2C%20("
                               ")&page=0&hitsPerPage=20".format(item)}

    def scrape_site(self):
        output = None
        try:
            response = requests.post(url='https://2fwotdvm2o-dsn.algolia.net/1/indexes/ProductTemplateSearch/query',
                                     headers=self.headers, params=self.params, json=self.data)
            output = json.loads(response.text)['hits'][0]

        except Exception as e:
            print(f'Error: {e}')
        return output