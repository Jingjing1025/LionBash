import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

region = 'us-east-1'
def lambda_handler(event, context):
    print(event)
    return_message = None
    if event['type'] == 'signup':
        q_res = queryFromDB(event['userId'], event['password']) # (keyword, whether account exist, response)
        if q_res[1]:
            return_message = "AccountExisted"
        else:
            storeToDB(event['userId'], event['password'], event['phone_number'], event['ip'])
            sendSNS(event['phone_number'], 'LionBash signup successful!')
            return_message = 'SignUpSuccess'
    elif event['type'] == 'login':
        q_res = queryFromDB(event['userId'], event['password']) # (keyword, whether account exist, response)
        if q_res[1]:
            if q_res[0]=='verified':
                updateDB(q_res[2]['Items'][0], event['ip'])
                return_message = 'LoginTrue'
            elif q_res[0]=='wrong':
                return_message = 'LoginFalse'
        else:
            return_message = 'NoAccount'
    print(return_message)
    return {
        'statusCode': 200,
        'body': return_message
    }
    
def storeToDB(userId, password, phone_number, ip):

    client = boto3.resource('dynamodb',
                      region_name=region,
                      aws_access_key_id='',
                      aws_secret_access_key='')
    table = client.Table('UserDB')

    try:
        response = table.put_item(
            TableName='UserDB',
            Item={
                'userId': userId,
                'password': password,
                'phone_number': phone_number,
                'ip':  ip 
            }
        )
    except Exception as err:
        print("Error storing to visitors db: ", err)

def updateDB(item, ip):
    client = boto3.resource('dynamodb',
                      region_name=region,
                      aws_access_key_id='',
                      aws_secret_access_key='')
    table = client.Table('UserDB')

    response = table.update_item(
    Key={
        "userId": item["userId"],
    },
    UpdateExpression="SET ip= :ip",
    ExpressionAttributeValues={
        ":ip": ip
    }
)

def queryFromDB(userId, password):
    client = boto3.resource('dynamodb',
                      region_name=region,
                      aws_access_key_id='',
                      aws_secret_access_key='')
    table = client.Table('UserDB')
    
    response = table.query(
    KeyConditionExpression=Key('userId').eq(userId)
    )
    
    print (response)
    
    if len(response['Items']) is not 0:
        if response['Items'][0]['password']==password:
            return ('verified', True, response)
        else:
            return ('wrong', True, response)
    return ('void', False, response)
    
def sendSNS(phone_number, message):
    sns = boto3.client('sns')
    response = sns.publish(
        PhoneNumber='+1'+phone_number,
        Message=message,
        Subject='AWS SNS test',
        MessageStructure='string'
    )
    print(response)
