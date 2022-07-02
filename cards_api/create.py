import json
import boto3
import os
import logging


dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CARDS_TABLE')
logger = logging.getLogger('Creat card')
logger.setLevel(logging.INFO)

#client = boto3.client('cognito-identity')
#client = boto3.client('cognito-idp')

def lambda_handler(event, context):
    card = json.loads(event['body'])
    table = dynamodb.Table(table_name)

    #users_id = client.get_id(IdentityPoolId='us-east-1:BevsnL9Sg')
    #users_id = context.cognito_identity_id 
    users_id = event[requestContext[requestId]]
    logger.info(users_id)

    response = table.put_item(
        TableName=table_name,
        Item={
            'id': card, #event['userAttributes'['sub']],
            'cardName': card['cardName'],
            'age': card['age'],
            'dob': card['dob'],
            'jobTitle': card['jobTitle'],
            'employer': card['employer'],
            'cityState': card['cityState'],
            'email': card['email'],
            'phoneNumber': card['phoneNumber']
        }
    )
    logger.info(response)
    return{
        'statusCode': 200,
        'headers': {
            #'Content-Type': 'application/json',

            #"Access-Control-Allow-Origin" : "*"
            #"Access-Control-Allow-Credentials": True

            #'Content-Type': 'application/json',
            #"Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
            #######"Access-Control-Allow-Origin": "*",
            #"Access-Control-Allow-Methods": "*",
            #"X-Requested-With": "*"

            #'Access-Control-Allow-Origin': 'http://localhost:3000',
            #'Access-Control-Allow-Credentials': 'True',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            #'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept',
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with", 
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps({'message': 'Business Card Created'})
    }