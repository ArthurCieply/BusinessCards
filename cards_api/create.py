import json
import boto3
import os
import logging
from jose import jwk, jwt
from jose.utils import base64url_decode
import urllib.request

# TODO: get params for region_id, userpool_id, app_client_id from environment for auth purposes?
# (SEE BELOW!)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CARDS_TABLE')
logger = logging.getLogger('Creat card')
logger.setLevel(logging.INFO)

# hanlder as defined in build.toml:
def lambda_handler(event, context):
    # authorization follows the example of https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py
    # (some modifications to pull in parameters from event object instead of setting statically)
    # get token:
    token = event['token']
    # get the 'kid' from the heads prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    # The following is pulled from https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
    # region (just pulled this from samconfig.toml)
    region_id = "us-east-1"
    # get user pool ID:
    userpool_id = event['userPoolId']

    # get the *app client id*:
    app_client_id = event['callerContext']['clientId']
    logger.info(app_client_id)
    keys_url = 'https://cognito-idp.{}.amazonaws.com/{}/.well-known/jwks.json'.format(region_id, userpool_id)

    # REVIEW: unlike in example from 'aws-support-tools', this will be run each time the lambda is called (not wise, but didn't want to mess setting static variables)
    with urllib.request.urlopen(keys_url) as f:
        response = f.read()
    keys = json.loads(response.decode('utf-8'))['keys']

    # now, search for the kid in the downloaded public keys:
    key_index = -1
    for i in range(len(keys)):
        if kid == keys[i]['kid']:
            key_index = i
            break
    if key_index == -1:
        print('Public key not found in jwks.json')
        return False

    # REVIEW: the following is just to illustrate that your authentication is working...
    # ... a 'real-life' example might utilize a separate lambda for this (???)
    # ... READ UP ON DOCS, LOOK FOR EXAMPLE CODE!!
    # construct the public key
    public_key = jwk.construct(keys[key_index])
    # get the last two sections of the token,
    # message and signature (encoded in base64)
    message, encoded_signature = str(token).rsplit('.', 1)
    # decode the signature
    decoded_signature = base64url_decode(encoded_signature.encode('utf-8'))
    # verify the signature
    if not public_key.verify(message.encode("utf8"), decoded_signature):
        print('Signature verification failed')
        return False
    print('Signature successfully verified')

    card = json.loads(event['body'])
    table = dynamodb.Table(table_name)


    # REVIEW: this is most likely wrong!
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
    # TODO: revisit after fixing authorization (see above!)
    # ... did not test at all!
    print("Response:", response)
    #logger.info(response)
    print("Event:", event)
    print("Context:", context)
    #   I think this will be the one I need to access sub but I'm going to start getting cognito to work before this because according to this there is no such thing as authorizers     print("Cognito sub:", event['requestContext']['authorizer']['claims']['sub'])
    #  Maybe this one  print("Sub:", context.authorizer.claims.sub)
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
        },
        'body': {
            json.dumps({'message': 'Business Card Created'})
        }
    }
