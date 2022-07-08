import simplejson as json
import boto3
import os
from boto3.dynamodb.conditions import Key
import logging


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CARDS_TABLE')
logger = logging.getLogger('patientcheckout')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    table = dynamodb.Table(table_name)
    #card_id = int(event['pathParameters']['id'])
    #response = table.query(KeyConditionExpression=Key('id').eq(card_id))
    response = table.scan()
    cards = response['Items']

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        cards.extend(response['Items'])

    #body = {
    #    'cards': cards
        #cards
    #}

    body = cards

    return{
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Content-Type": "application/json",
            "X-Requested-With": "*"
        },
        #'body': json.dumps(response['Items'])
        'body': json.dumps(body)
    }