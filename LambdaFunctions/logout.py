import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
region = 'us-east-1'

def lambda_handler(event, context):
    if queryFromDB(event["ip"]) is None:
        return {
        'statusCode': 200,
        'body': "Fail"
    }
    updateDB(event["ip"])
    return {
        'statusCode': 200,
        'body': "Success"
    }



def updateDB(ip):
    client = boto3.resource('dynamodb',
                      region_name=region,
                      aws_access_key_id='',
                      aws_secret_access_key='')
    table = client.Table('UserDB')

    response = table.update_item(
    Key={
        "userId": queryFromDB(ip)
    },
    UpdateExpression="SET ip= :ip",
    ExpressionAttributeValues={
        ":ip": "null"
    }
)

def queryFromDB(user_ip):
    client = boto3.resource('dynamodb',
                      region_name=region,
                      aws_access_key_id='',
                      aws_secret_access_key='')
    table = client.Table('UserDB')
    
    response = table.scan(FilterExpression=Key('ip').eq(user_ip))
    
    print (response)
    
    if len(response['Items']) is not 0:
        uni = response['Items'][0]['userId']
        return (uni)
    return None