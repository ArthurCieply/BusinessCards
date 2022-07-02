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
    card_id = int(event['pathParameters']['id'])
    response = table.delete_item(Key={'id': card_id})
    #response = table.delete_item(KeyConditionExpression=Key('id').eq(card_id))
    logger.info(response)
    return{
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin" : "http://localhost:3000/",
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH" 
            #"Access-Control-Allow-Credentials": True
        },
        'body': json.dumps({'message': 'Business Card Deleted'})
    }