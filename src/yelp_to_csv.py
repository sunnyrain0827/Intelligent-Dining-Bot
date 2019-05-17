import csv
import boto3
import json
import datetime
from urllib.parse import quote
from botocore.vendored import requests

dynamodb = boto3.resource('dynamodb', 'us-east-1')

# Yelp API
API_KEY = "UaWHMi_1xqrL892PWXiNDw_t0-reTr-k98w07gwN4wEH0ivIlyDtoOCM28zjg03_MYCIIDywM6wIz3HQZDxBWVRUEdsEl2jnlw1Gu_uuzixFSf2cY58HGc0GGgiDXHYx"
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'


# def read_csv(csv_file, l):
#     rows = csv.DictReader(open(csv_file))
#     for row in rows:
#         l.append(row)


def write_to_csv(file_name, items):
    print(items)
    businesses = items['businesses']
    print(businesses)
    with open(file_name, 'a') as newFile:
        newFileWriter = csv.writer(newFile)
        for i in range(len(businesses)):  # for each restaurant dictionary
            # for key, value in item.items():
            #     if not value:
            #         item[key] = -1
            # add timestamp
            # item['insertedAtTimestamp'] = str(datetime.datetime.now())
            # print(item)
            try:
                newFileWriter.writerow([businesses[i]['id'], businesses[i]['name'], 'spanish',
                                        businesses[i]['location']['display_address'][0] + ', '
                                        + businesses[i]['location']['display_address'][1],
                                        str(businesses[i]['coordinates']['latitude']) + ',' + str(
                                            businesses[i]['coordinates']['longitude']),
                                        businesses[i]['review_count'],
                                        businesses[i]['rating'],
                                        businesses[i]['location']['zip_code']
                                        ])
            except UnicodeEncodeError:
                continue

            except IndexError:
                continue

            # batch.put_item(Item={'business_id': businesses['id'], 'name': businesses['name'], 'cuisine': 'japanese',
            #                      'address': businesses['location']['address1'], 'coordinates':
            #                          '(' + region['center']['latitude'] + ',' + ')', 'number_of_reviews': businesses['review_count'],
            #                      'rating': businesses['rating'], 'zip_code': businesses['location']['zip_code']
            #                      })


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


if __name__ == '__main__':
    file_name = 'sample_csv.csv'
    url_params = {}
    url_params["location"] = "bronx"
    url_params["term"] = "spanish"
    url_params["limit"] = 2
    i = 0
    # while i <= 950:
    #     res = request(API_HOST, SEARCH_PATH, API_KEY, url_params)
    #     write_to_csv(file_name, res)
    #     i += 50
    #     url_params["offset"] = i
    #     print(i)

    # make sure go beyond 1000
    url_params["offset"] = 998
    res = request(API_HOST, SEARCH_PATH, API_KEY, url_params)
    write_to_csv(file_name, res)