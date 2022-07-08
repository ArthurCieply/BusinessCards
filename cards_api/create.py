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
    #users_id = event[requestContext[requestId]]
    #users_id = context['identity']
    #logger.info(users_id)

    print("Lambda Request ID:", context.aws_request_id)

    response = table.put_item(
        TableName=table_name,
        Item={
            'id': str(context.aws_request_id),#card, #event['userAttributes'['sub']],
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
    print("Response:", response)
    #logger.info(response)
    print("Event:", event)
    print("Context:", context)
    #   I think this will be the one I need to access sub but I'm going to start getting cognito to work before this because according to this there is no such thing as authorizers     print("Cognito sub:", event['requestContext']['authorizer']['claims']['sub'])
    #  Maybe this one  print("Sub:", context.authorizer.claims.sub)
    #print("Sub:", context.authorizer.claims.sub)
    #print("Context.Identity :", context.identity) #event.requestContext.authorizer.claims.sub) #context.authorizer.claims.sub )
    #print("Sub:", event.requestContext.identity.cognitoIdentityId) #event.requestContext.authorizer.claims.sub) #context.authorizer.claims.sub )
    return{
        'statusCode': 200,
        'cors': True,
        'headers': {
            "Access-Control-Allow-Origin" : "http://localhost:3000",#"*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT",
            "Content-Type": "application/json",
            "X-Requested-With": "*"


            #'Content-Type': 'application/json',

            #"Access-Control-Allow-Origin" : "*"
            #"Access-Control-Allow-Credentials": True

            #'Content-Type': 'application/json',
            #"Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,X-Amz-Security-Token,Authorization,X-Api-Key,X-Requested-With,Accept,Access-Control-Allow-Methods,Access-Control-Allow-Origin,Access-Control-Allow-Headers",
            #######"Access-Control-Allow-Origin": "*",
            #"Access-Control-Allow-Methods": "*",
            #"X-Requested-With": "*"

            #'Access-Control-Allow-Origin': 'http://localhost:3000',
            #'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept',


            #'Access-Control-Allow-Credentials': True,
            #'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            #"Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with", 
            #"Content-Type": "application/json",
            #"Access-Control-Allow-Origin": "*",
            #"X-Requested-With": "*"
        },
        'body': {
            json.dumps({'message': 'Business Card Created'})
        }
    }