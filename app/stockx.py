import json
import requests
from datetime import datetime


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-gb",
    "content-type": "application/json; charset=utf-8"
}


def find_item(item):
    '''
    Returns the name and product ids of a searched sneaker
    '''
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}

    params = {
        'x-algolia-agent': 'Algolia for JavaScript (4.9.1); Browser',
        'x-algolia-api-key': 'OWM2ZDFkN2E0YjlkNzZmYmZkYTRiMTAyYzBhMTU4ZTI1NDI2Zjg5OWM3NDU0YzhiZDIyZmMyYmQ3NDk5NmNiOXZhbGlkVW50aWw9MTYyNTM1MTQ0Nw==',
        'x-algolia-application-id': 'XW7SBCT9V6'
    }

    data = {"params": "query={}&hitsPerPage=20&facets=*".format(item)}

    response = requests.post(url='https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query', headers=headers,  params=params, json=data)
    output = json.loads(response.text)

    hits = []
    for i in output['hits']:
        hits.append([i['name'], i['objectID']])
    return hits


def get_product_details(item):
    '''
    Returns the title and image url of a sneaker
    '''
    #headers = {'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"}
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
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}

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



# Use for testing purposes
if __name__ == '__main__':
    item = find_item('yeezy')
    print(item)