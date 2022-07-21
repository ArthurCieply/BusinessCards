import json
import boto3
import os
import logging
from jose import jwk, jwt
from jose.utils import base64url_decode
import urllib.request
from uuid import uuid4


# TODO: get params for region_id, userpool_id, app_client_id from environment for auth purposes?
# (SEE BELOW!)
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('CARDS_TABLE')
logger = logging.getLogger('Creat card')
logger.setLevel(logging.INFO)

#def set_default(obj):
#    if isinstance(obj, set):
#        return list(obj)
#    raise TypeError

# hanlder as defined in build.toml:
def lambda_handler(event, context):
    print("Event: ", event)
    print("Context: ", context)
    id_token = event["headers"]["Authorization"]
    id_token = id_token[7:]
    token = id_token
    # authorization follows the example of https://github.com/awslabs/aws-support-tools/blob/master/Cognito/decode-verify-jwt/decode-verify-jwt.py
    # (some modifications to pull in parameters from event object instead of setting statically)
    # get token:
    #   Substituted for above    token = event['token']
    # get the 'kid' from the heads prior to verification
    headers = jwt.get_unverified_headers(token)
    kid = headers['kid']

    # The following is pulled from https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-post-authentication.html
    # region (just pulled this from samconfig.toml)
    region_id = "us-east-1"
    # get user pool ID:
    #userpool_id = event['userPoolId']
    userpool_id = "us-east-1_yHJhy2Fkd"

    # get the *app client id*:
    ########   No callerContext or clientID in event     app_client_id = event['callerContext']['clientId']
    #                   logger.info(app_client_id)
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

    sub = event["requestContext"]["authorizer"]["claims"]["sub"]
    print("sub:", sub)

    response = table.put_item(
        TableName=table_name,
        Item={
            'id': sub,
            'sort': str(uuid4().hex),
            'cardName': card['cardName'],
            'age': card['age'],
            'dob': card['dob'],
            'jobTitle': card['jobTitle'],
            'employer': card['employer'],
            'cityState': card['cityState'],
            'email': card['email'],
            'phoneNumber': card['phoneNumber'],
            'pictureName': card['pictureName']
        }
    )
    # TODO: revisit after fixing authorization (see above!)
    # ... did not test at all!
    print("Response:", response)
    
    multi_value_headers = {"Access-Control-Allow-Origin" : ["http://localhost:3000"], "Access-Control-Allow-Credentials": [True], "Access-Control-Allow-Headers" : ["Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with"], "Access-Control-Allow-Methods": ["GET, POST, OPTIONS, PUT"], "Content-Type": ["application/json"], "X-Requested-With": ["*"]}
    return{
        'statusCode': 200,
        #'cors': True,
        #'headers': {
        #    "Access-Control-Allow-Origin" : "http://localhost:3000",#"*",
        #    "Access-Control-Allow-Credentials": True,
        #    "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with",
        #    "Access-Control-Allow-Methods": "GET, POST, OPTIONS, PUT",
        #    "Content-Type": "application/json",
        #    "X-Requested-With": "*"
        #},
        #'multiValueHeaders': {"Access-Control-Allow-Origin" : ["http://localhost:3000"], "Access-Control-Allow-Credentials": [True], "Access-Control-Allow-Headers" : ["Content-Type,X-Amz-Date,Authorization,X-Api-Key,x-requested-with"], "Access-Control-Allow-Methods": ["GET, POST, OPTIONS, PUT"], "Content-Type": ["application/json"], "X-Requested-With": ["*"]},
        'multiValueHeaders': multi_value_headers,
        'body': json.dumps({'message': 'Business Card Created'})
        #'body': {
            #json.dumps({"Business Card Created"})
            #json.dumps({'message': 'Business Card Created'})
            #json.dumps({'message': 'Business Card Created'}, default=str)
            #json.dumps({'message': 'Business Card Created'}, default=set_default)
        #}
    }
