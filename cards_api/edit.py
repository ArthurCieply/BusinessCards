import json
import boto3
import os
import logging


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CARDS_TABLE')
logger = logging.getLogger('patientcheckout')
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    card = json.loads(event['body'])
    table = dynamodb.Table(table_name)
    card_id = int(event['pathParameters']['id'])
    response = table.put_item(TableName=table_name, Item=card)
    logger.info(response)
    return{
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "http://localhost:3000/",
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with"
        },
        'body': json.dumps({'message': 'Business Card Created'})
    }