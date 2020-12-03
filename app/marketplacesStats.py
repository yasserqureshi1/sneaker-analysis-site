import requests
from bs4 import BeautifulSoup
import statistics
import json


class EbayPriceChecker:
    def __init__(self, item, proxy=None):
        self.item = item
        if proxy is None:
            self.proxies = {}
        else:
            self.proxies = proxy

    def get_current_prices(self):
        current_listings = []
        try:
            url = f'https://www.ebay.co.uk/sch/i.html?_nkw={self.item.replace(" ", "+")}&_ipg=200'
            html = requests.get(url=url, proxies=self.proxies)
            soup = BeautifulSoup(html.text, 'html.parser')

            for product in soup.find_all('div', {'class': 's-item__wrapper clearfix'}):
                price = product.find('span', {'class': 's-item__price'}).text
                try:
                    current_listings.append(float(price.replace('£', '')))
                except:
                    price = price.replace(' to', '').replace('£', '')
                    price = price.split()
                    prices = [float(item) for item in price]
                    current_listings.append(statistics.mean(prices))
        except:
            print('Error occurred')
        return current_listings

    def get_sold_prices(self):
        sold_listings = []
        try:
            url = f'https://www.ebay.co.uk/sch/i.html?_nkw={self.item.replace(" ", "+")}&_ipg=200&rt=nc&LH_Sold=1'
            html = requests.get(url=url, proxies=self.proxies)
            soup = BeautifulSoup(html.text, 'html.parser')
            for product in soup.find_all('div', {'class': 's-item__wrapper clearfix'}):
                price = product.find('span', {'class': 's-item__price'}).text
                try:
                    sold_listings.append(float(price.replace('£', '')))
                except:
                    price = price.replace(' to', '').replace('£', '')
                    price = price.split()
                    sold_listings.append(statistics.mean([float(item) for item in price]))
        except:
            print('Error occurred')
        return sold_listings


class DepopPriceChecker:
    def __init__(self, item, proxies=None):
        self.item = item
        if proxies == None:
            self.proxies = {}
        else:
            self.proxies = proxies

    def scrape_site(self):
        current_listings = []
        try:
            url = f'https://webapi.depop.com/api/v1/search/?what={self.item.replace(" ", "%20")}&country=gb&limit=200'
            html = requests.get(url=url, proxies=self.proxies).text
            output = json.loads(html)
            for i in output['products']:
                price = i['price']['price_amount']
                current_listings.append(float(price))
        except:
            print('error')
        return current_listings

    def get_current_prices(self):
        current_listings = self.scrape_site()
        mean = statistics.mean(current_listings)
        std = statistics.stdev(current_listings)
        for item in current_listings:
            if item > (mean + std / 2) or item < (mean - std / 2):
                current_listings.remove(item)
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
            output = json.loads(response.text)
        except:
            print('Error Occurred')
        return output

    def get_current_listing_stats(self):
        output = self.scrape_site()
        new_lowest_price_cents = int(output['hits'][0]['new_lowest_price_cents'] / 100)
        maximum_offer = int(output['hits'][0]['maximum_offer_cents'] / 100)
        minimum_offer = int(output['hits'][0]['minimum_offer_cents'] / 100)
        used_lowest_price_cents = int(output['hits'][0]['used_lowest_price_cents'] / 100)
        want_count = output['hits'][0]['want_count']
        want_count_three = output['hits'][0]['three_day_rolling_want_count']
        return new_lowest_price_cents, maximum_offer, minimum_offer, used_lowest_price_cents, want_count, want_count_three


class BumpPriceChecker:
    def __init__(self, item, proxies=None):
        self.item = item
        self.current_listings = []
        if proxies == None:
            self.proxies = []
        else:
            self.proxies = proxies

    def get_current_prices(self):
        current_listings = []
        try:
            url = f'https://sobump.com/search?q={self.item.replace(" ", "%20")}'
            html = requests.get(url=url, proxies=self.proxies).text
            soup = BeautifulSoup(html, 'html.parser')

            for item in soup.find_all('div', {'class': 'product-search-container_product-container__price__22GHm'}):
                current_listings.append(float(item.text.replace('£', '')))
        except:
            print('Error occurred')
        return current_listings


def stats(array):
    return statistics.mean(array), statistics.mode(array), max(float(sub) for sub in array), min(float(sub) for sub in array)


if __name__ == '__main__':
    mean, mode, maximum, minimum = stats(DepopPriceChecker('yeezy zyon').get_current_prices())
    print(mean, mode, maximum, minimum)
    print(' ')

    mean, mode, maximum, minimum = stats(EbayPriceChecker('yeezy zyon').get_current_prices())
    print(mean, mode, maximum, minimum)
    print(' ')

    mean, mode, maximum, minimum = stats(BumpPriceChecker('yeezy zyon').get_current_prices())
    print(mean, mode, maximum, minimum)
