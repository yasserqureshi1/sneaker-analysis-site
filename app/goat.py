import requests
import json


headers = {'accept': 'application/json',
           'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}
params = {'x-algolia-agent': 'Algolia for JavaScript (3.35.1); Browser',
          'x-algolia-api-key': 'ac96de6fef0e02bb95d433d8d5c7038a',
          'x-algolia-application-id': '2FWOTDVM2O'}
url = 'https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2_trending_purchase/query'


def find_item(item):
    data = {"params": "query={}&distinct=true&facetFilters=(product_category%3Ashoes)&page=0&hitsPerPage=20&clickAnalytics=true".format(item.replace(' ', '%20'))}
    html = requests.post(url=url, headers=headers, params=params, json=data)
    output = json.loads(html.text)
    shoes = []
    for shoe in output['hits']:
        shoes.append({
            "name": shoe['name'],
            "sku": shoe['sku'],
            "picture_url": shoe['original_picture_url']
        })
    return shoes


def get_shoe_details(item):
    '''Indexes into the JSON object returned by the scrape_site() function to return a dictionary with specific data'''
    data = {"params": "query={}&distinct=true&facetFilters=(product_category%3Ashoes)&page=0&hitsPerPage=20&clickAnalytics=true".format(item.replace(' ', '%20'))}
    html = requests.post(url=url, headers=headers, params=params, json=data)
    output = json.loads(html.text)
    try:
        data = {
            'name': output['hits'][0].get('name'),
            'sku': output['hits'][0].get('sku'),
            'picture_url': output['hits'][0].get('original_picture_url'),
            'colour': output['hits'][0].get('color'),
            'details': output['hits'][0]['details'],
            'release_date': output['hits'][0]['release_date'],
            'midsole': output['hits'][0]['midsole'],
            'upper_material': output['hits'][0]['upper_material'],
            'designer': output['hits'][0]['designer'],
            'silhouette': output['hits'][0]['silhouette']
        }
    except Exception as e:
        try:
            print(e)
            data = {
                'name': output['hits'].get('name'),
                'sku': output['hits'].get('sku'),
                'colour': output['hits'].get('color'),
                'details': output['hits'].get('details'),
                'release_date': output['hits'].get('release_date'),
                'midsole': output['hits'].get('midsole'),
                'upper_material': output['hits'].get('upper_material'),
                'designer': output['hits'].get('designer'),
                'silhouette': output['hits'].get('silhouette')
            }
        except Exception as ee:
            print(ee)
            data = {
                'name': None,
                'sku': None,
                'colour': None,
                'details': None,
                'release_date': None,
                'midsole': None,
                'upper_material': None,
                'designer': None,
                'silhouette': None
            }
    return data


# Use for testing purposes
if __name__ == '__main__':
    find_item('yeezy')
    #print(get_shoe_details('FU9013'))

    #shoes = find_item('yeezy')
    #for shoe in shoes:
    #    print(shoe)