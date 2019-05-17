import json
import boto3
import json
import sys
import http.client

def search(uri, term):
    """Simple Elasticsearch Query"""
    conn = http.client.HTTPSConnection("search-restruantelastic-ktezaxacx6oxs4l5bysjlgi454.us-east-1.es.amazonaws.com")
    conn.request(method = "GET", url = "/restaurants/_search?q=cuisine:"+term)
    results = conn.getresponse()
    return results

def lambda_handler(event, context):
    client = boto3.client('sqs')
    # TODO implement
    response = client.receive_message(
    QueueUrl='https://sqs.us-east-1.amazonaws.com/418020433931/restaurantQueue',
    AttributeNames=[
        'All'
    ],
    MessageAttributeNames=[
        'number', 
        'date',
        'my_time',
        'cuisine',
        'phone'
    ]
    )
    cuisine = response['Messages'][0]['MessageAttributes']['cuisine']['StringValue']
    number = response['Messages'][0]['MessageAttributes']['number']['StringValue']
    date = response['Messages'][0]['MessageAttributes']['date']['StringValue']
    my_time = response['Messages'][0]['MessageAttributes']['my_time']['StringValue']
    phone = response['Messages'][0]['MessageAttributes']['phone']['StringValue']
    
    
    result = search("https://search-restruantelastic-ktezaxacx6oxs4l5bysjlgi454.us-east-1.es.amazonaws.com", cuisine)
    result = json.load(result)
    busID_list = result['hits']['hits'][:4]
    client3 = boto3.client('dynamodb')
    address = []
    name = []
    for i in range(4):
        response3 = client3.get_item(
        TableName='yelp-restaurants',
        Key={
            'business_id': {
                'S': busID_list[i]['_id']
            }
        },
        )['Item']
        address.append(response3["address"]["S"])
        name.append(response3["name"]["S"])
        
    
    client5 = boto3.client('sns')
    response5 = client5.publish(
    PhoneNumber='+1'+phone,
    Message='Hello! Here are my {} restaurant suggestions for {} people, for {} at {}: 1. {}, located at {}; 2. {}, located at {}; 3. {}, located at {}'.format(cuisine, number, date, my_time, name[0], address[0], name[1], address[1], name[2], address[2]),
    Subject='Concierge'
    )
    return {
        'statusCode': 200,
        'body': response['Messages'][0]['MessageAttributes']['phone']['StringValue']
    }
