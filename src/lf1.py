import math
import boto3
import dateutil.parser
import datetime
import time
import os
import logging
import json
from botocore.vendored import requests
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Yelp API
API_KEY = "UaWHMi_1xqrL892PWXiNDw_t0-reTr-k98w07gwN4wEH0ivIlyDtoOCM28zjg03_MYCIIDywM6wIz3HQZDxBWVRUEdsEl2jnlw1Gu_uuzixFSf2cY58HGc0GGgiDXHYx"
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'


def close(session, fulfill, m):
    response = {
        'sessionAttributes': session,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfill,
            'message': m
        }
    }
    return response


def fetch(intent_request):
    return intent_request['currentIntent']['slots']


def assign(session, slots):
    return {
        'sessionAttributes': session,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def dining(intent_request):
    location = fetch(intent_request)["location"]
    date = fetch(intent_request)["date"]
    my_time = fetch(intent_request)["time"]
    cuisine = fetch(intent_request)["cuisine"]
    number = fetch(intent_request)["number"]
    phone = fetch(intent_request)["phone"]
    source = intent_request['invocationSource']
    if source == 'DialogCodeHook':
        output_session = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        # return assign(output_session, fetch(intent_request))

    # number = 1
    # date = "today"
    # my_time = "7pm"
    # cuisine = "japanese"
    # email_address = "tw2576@columbia.edu"
    client = boto3.client('sqs')
    response = client.send_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/418020433931/restaurantQueue',
        # DelaySeconds=2,
        MessageAttributes={
            'number': {
                'StringValue': str(number),
                'DataType': 'String'
            },
            'date': {
                'StringValue': str(date),
                'DataType': 'String'
            },
            'my_time': {
                'StringValue': str(my_time),
                'DataType': 'String'
            },
            'cuisine': {
                'StringValue': str(cuisine),
                'DataType': 'String'
            },
            'phone': {
                'StringValue': str(phone),
                'DataType': 'String'
            },
        },
        MessageBody="{'number': {'StringValue': str(number), 'DataType': 'String'}, 'date': {'StringValue': str(date), 'DataType': 'String'}, 'my_time': {'StringValue': str(my_time), 'DataType': 'String'}, 'cuisine': {'StringValue': str(cuisine), 'DataType': 'String'}, 'phone': {'StringValue': str(phone), 'DataType': 'String'}}"
    )
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 # {'contentType': 'PlainText',
                 #  'content':'These are {} restaurant recommendations for {} people, for {} at {}. {} at {}; {} at {}; {} at {}'.format(cuisine,number,date,my_time,res[0][0],res[0][1],res[1][0],res[1][1],res[2][0],res[2][1])})
                 {'contentType': 'PlainText',
                  'content': 'You are all set. Expect my recommendations shortly! Have a good day.'})


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    shortresponse = response.json()["businesses"][0:3]
    res = []
    for e in shortresponse:
        temp = []
        temp.append(e["name"])
        temp.append(e["location"]["address1"])
        res.append(temp)

    return res


""" --- Intents --- """


def dispatch(intent_request):
    logger.debug(
        'dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    if intent_name == 'DiningSuggestions':
        return dining(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))
    return dispatch(event)