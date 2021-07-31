import json
import requests
from datetime import datetime


headers= {
    "accept": "application/json",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "origin": "https://www.apirequest.io",
    "referer": "https://www.apirequest.io/",
    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
}


def find_item(item):
    '''
    Returns the name and product ids of a searched sneaker
    '''
    params = {
        'x-algolia-agent': 'Algolia for JavaScript (4.9.1); Browser',
        'x-algolia-api-key': 'ZDUyZTFlNjBjNTMxZjM2YTZhZjcxYTkxNzY1Y2FkMzgxYmIwNzZjMjJiYmEzNGZhNTlkMWE4NDYyNzM0ZjcwY3ZhbGlkVW50aWw9MTYyNzkwNjk5Mw==',
        'x-algolia-application-id': 'XW7SBCT9V6'
    }

    data = {"params": "query={}&hitsPerPage=20&facets=*".format(item)}

    response = requests.post(url='https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query', headers=headers,  params=params, json=data)
    output = json.loads(response.text)

    hits = []
    for i in output['hits']:
        hits.append({
            'name': i['name'], 
            'sku': i['objectID'],
            'picture_url': i['thumbnail_url']
            })
    return hits


def get_product_details(item):
    '''
    Returns the title and image url of a sneaker
    '''
    url = f'https://stockx.com/api/products/{item}'
    response = requests.get(url=url, headers=headers)
    output = json.loads(response.text)
    data = {'title': output['Product']['title']}
    try:
        data['image_url'] = output['Product']['media']['360'][0]
    except:
        data['image_url'] = output['Product']['media']['imageUrl']
    data['colourway'] = output['Product']['colorway']
    data['brand'] = output['Product']['brand']
    data['release_date'] = output['Product']['releaseDate']
    data['retail_price'] = output['Product']['retailPrice']
    return data


def get_datapoints(item_id):
    '''
    Returns the 500 datapoints corresponding to previous historical prices
    '''
    no_of_points = 500  # MAX IS 500
    current_date = datetime.date(datetime.now())
    url = f'https://stockx.com/api/products/{item_id}/chart?start_date=all&end_date={current_date.year}-{current_date.month}-{current_date.day}&intervals={str(no_of_points)}&format=highstock&currency=GBP&country=GB'
    outputs = json.loads(requests.get(url=url, headers=headers).text)
    return outputs['series'][0]['data']


def get_related(item_id):
    '''
    Returns related sneakers
    '''
    url = f'https://stockx.com/api/products/{item_id}/related?currency=GBP&limit=15&country=GB'
    response = requests.get(url=url, headers=headers) # Returns all details on 15 related shoes
    print(response.text)


def get_prices(item_id):
    '''
    Returns StockX market
    '''
    url = f'https://stockx.com/api/products/{item_id}/market?currency=GBP&country=GB'
    response = requests.get(url=url, headers=headers)
    output = json.loads(response.text)
    return output['Market']



# Use for testing purposes
if __name__ == '__main__':
    print(get_prices('117a507b-f50a-493b-9ce2-b71b42ccad06'))