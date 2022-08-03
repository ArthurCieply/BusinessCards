import simplejson as json
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
    #card_id = int(event['pathParameters']['id'])
    card_id = str(event['pathParameters']['id'])
    card_sort = str(event['pathParameters']['sort'])
    update_key = card['updateKey']
    update_value = card['updateValue']
    response = table.update_item(
        Key={
            'id': card_id
        },
        UpdateExpression="set %s = :value" % update_key,
        ExpressionAttributeValues={
            ":value": update_value
        },
        ReturnValues="UPDATED_NEW"
    )
    logger.info(response)
    #return{
    #    'statusCode': 200,
    #    'headers': {
    #        "Access-Control-Allow-Origin" : "*",
    #        #"Access-Control-Allow-Credentials": True
    #        "Access-Control-Allow-Methods": "OPTIONS,POST,GET,PUT,DELETE,PATCH",
    #        "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with"
    #    },
    #    'body': json.dumps({'message': 'Business Card Updated'})
    #}