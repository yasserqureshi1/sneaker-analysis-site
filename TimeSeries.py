import json
import requests
import matplotlib.pyplot as plt
import time


class TimeSeries:
    def __init__(self, item):
        self.item = item
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0"}
        self.params = {'x-algolia-agent': 'Algolia for vanilla JavaScript 3.22.1',
                       'x-algolia-api-key': '6bfb5abee4dcd8cea8f0ca1ca085c2b3',
                       'x-algolia-application-id': 'XW7SBCT9V6'}
        self.id = []
        self.list = []

    def findItem(self):
        data = {"params": "query={}&hitsPerPage=20&facets=*".format(self.item)}

        response = requests.post(url='https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query',
                                 headers=self.headers,
                                 params=self.params, json=data)
        output = json.loads(response.text)

        for i in output['hits']:
            print(i['name'])
            print(i['objectID'], '\n')
            self.id.append(i['objectID'])

    def getData(self):
        no_of_points = 500  # MAX IS 500

        url = 'https://stockx.com/api/products/' + str(self.id[0]) + '/chart?start_date=all&end_date=2020-07-15' \
            '&intervals=' + str(no_of_points) + '&format=highstock&currency=GBP&country=GB '
        outputs = json.loads(requests.get(url, headers=self.headers).text)

        for i in outputs['series']:
            self.list = i['data']

        return self.list

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


if __name__ == '__main__':
    shoe = TimeSeries('yeezy zyon')
    shoe.main()
