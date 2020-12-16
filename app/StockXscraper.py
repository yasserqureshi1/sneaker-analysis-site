import json
import requests
import matplotlib.pyplot as plt
import time

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}

params = {'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
                       'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3',
                       'x-algolia-application-id': 'XW7SBCT9V6'}


def findItem(item):
    '''
    Returns the name and product ids of a searched sneaker
    '''
    data = {"params": "query={}&hitsPerPage=20&facets=*".format(item)}

    response = requests.post(url='https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query', headers=headers,  params=params, json=data)
    output = json.loads(response.text)

    hits = []
    for i in output['hits']:
        print(i['name'])
        print(i['objectID'], '\n')
        hits.append([i['name'], i['objectID']])
    return hits


def getProductDetails(item):
    '''
    Returns the title and image url of a sneaker
    '''
    url = f'https://stockx.com/api/products/{item}'
    response = requests.get(url=url, headers=headers)
    output = json.loads(response.text)
    title = output['Product']['title']
    try:
        image_url = output['Product']['media']['360'][0]
    except:
        image_url = output['Product']['media']['imageUrl']
    return [title, image_url]


def getDatapoints(item_id):
    '''
    Returns the 500 datapoints corresponding to previous historical prices
    '''
    no_of_points = 500  # MAX IS 500
    url = f'https://stockx.com/api/products/{item_id}/chart?start_date=all&end_date=2020-07-15&intervals={str(no_of_points)}&format=highstock&currency=GBP&country=GB'
    outputs = json.loads(requests.get(url=url, headers=headers).text)
    return outputs['series']['data']

def getRelated(item_id):
    '''
    Returns related sneakers
    '''
    url = f'https://stockx.com/api/products/{item_id}/related?currency=GBP&limit=15&country=GB'
    response = requests.get(url=url, headers=headers) # Returns all details on 15 related shoes
    print(response.text)

def getFeatures(item_id):
    pass


def epoch2human(self, epoch):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(epoch) / 1000.0))


def conversion(self, list):
    x, y = zip(*list)
    x = [self.epoch2human(t) for t in x]
    return x, y


def plot(self, x, y):
    fig = plt.figure(figsize=(10, 8), dpi=80)
    plt.plot(x, y)
    plt.tick_params(axis='both', which='major', labelsize=8)
    plt.show()


def main(self):
    self.findItem()
    self.getData()
    x, y = self.conversion(self.list)
    self.plot(x, y)

if __name__ == "__main__":
    item = findItem('Yeezy Zebra')
    getRelated(item[0][1])