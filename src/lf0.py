import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    id = "bot"
    client = boto3.client('lex-runtime')
    response = client.post_text(botName="DiningC", 
                                botAlias="diningBot", 
                                userId= id + event.get("id_token"),  
                                inputText=event.get("Data"))
    msg = response.get("message")
    return {
        'statusCode': 200,
        'body': json.dumps(msg)
    }