import boto3
import json
import random
from datetime import datetime
import time
from boto3.dynamodb.conditions import Key, Attr
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = ''
index = 'events'
url = host + '/' + index + '/_search'

headers = { "Content-Type": "application/json" }


def sendSNS(phone_number, message):
    # Create an SNS client
    sns = boto3.client('sns')
    
    # Publish a simple message to the specified SNS topic
    response = sns.publish(
        PhoneNumber="+1"+phone_number,
        Message=message,
        Subject='AWS SNS test',
        MessageStructure='string'
    )
    
    # Print out the response
    print("SNS response:", response)

def queryFromES(category, phone_number):
    
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    print("category: ", category)
    
    query = {
        "size": 3,
        "query": {
            "match": {
                "Category": category
            }
        }
    }

    # Make the signed HTTP request
    found_results = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    events_id = []
    events_location = []
    
    try:
        res = json.loads(found_results.text)
        for hit in res['hits']['hits']:
            id = hit['_source']['Name']
            name = id.replace("_", " ")
            events_id.append(name)
            events_location.append(hit['_source']['Location'])
        
        name1 = events_id[0]
        name2 = events_id[1]
        name3 = events_id[2]
        address1 = events_location[0]
        address2 = events_location[1]
        address3 = events_location[2]
 
        output = "Hello! Here are my " + category + " events suggestions: 1. " + name1 + ", located at " + address1 + ", 2. " + name2 + ", located at " + address2 + ", 3. " + name3 + ", located at " + address3 + ". Have Fun!"
        print(output)
        sendSNS(phone_number, output)
    
    except:
        output = "Sorry, we don't currently have events that match your queries right now. Would you like to try a different search?"
        print(output)
        sendSNS(phone_number, output)
        return(ouput)

    return


# Lambda execution starts here
def lambda_handler(event, context):
    print(event)
    
    for record in event['Records']:
       msg=record["body"]
       eventInfo = json.loads(msg)
       category = eventInfo["Category"]
       phone_number = eventInfo['PhoneNumber']

    events_found = queryFromES(category, phone_number)

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        'body' : json.dumps(events_found),
        "isBase64Encoded": False
    }

    return response