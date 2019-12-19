import boto3
import json
import random
from datetime import datetime
import time
from boto3.dynamodb.conditions import Key, Attr, And
import requests
from requests_aws4auth import AWS4Auth

region = 'us-east-1' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = ''
index = 'events'
store_type = '_doc'
search_type = '_search'
update_type = '_update_by_query'

headers = { "Content-Type": "application/json" }

def queryFromDB(user_ip):
    client = boto3.resource('dynamodb',
                      region_name=region,
                      aws_access_key_id='',
                      aws_secret_access_key='')
    table = client.Table('UserDB')
    
    response = table.scan(FilterExpression=Key('ip').eq(user_ip))
    
    print (response)
    
    if len(response['Items']) != 0:
        uni = response['Items'][0]['userId']
        phone_number = response['Items'][0]['phone_number']
        return (uni, phone_number)
    print("queried phone_number:", phone_number)
    return ('None', 'None')


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

def queryFromES_category(category):
    
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    print("category: ", category)
    
    query = {
        "query": {
            "match": {
                "Category": category
            }
        }
    }

    url = host + '/' + index + '/' + search_type
    # Make the signed HTTP request
    found_results = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    events_result = {}
    count = 0
    try:
        res = json.loads(found_results.text)
        for hit in res['hits']['hits']:
            events_result[str(count)] = hit['_source']
            count += 1
            
        print(events_result)
    except:
        return events_result

    return events_result


def queryFromES_user(user):
    
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    print("user: ", user)
    
    query = {
        "query": {
        "bool": {
            "filter": {
                "term": {
                    "RelatedUsers": user
                }
            }
        }
        }
    }

    url = host + '/' + index + '/' + search_type
    # Make the signed HTTP request
    found_results = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))
    events_result = []
    try:
        res = json.loads(found_results.text)
        print(res)
        for hit in res['hits']['hits']:
            events_result.append(hit['_source'])
        
        print(events_result)
        
    except:
        return events_result

    return events_result


def storeToES(event_name, event_date, event_time, event_location, event_detail, category, photo, creator, phone_number):
    timestamp = int(time.time())
    event_id = event_name.replace(" ", "") + str(timestamp) 
            
    document = {
        "ID": event_id,
        "Name": event_name,
        "Date": event_date,
        "Time": event_time,
        "Location": event_location,
        "Detail": event_detail,
        "Category": category,
        "CreatorPhone": phone_number,
        "Photo": photo,
        "RelatedUsers": [creator]
    }
    print(document)
    
    url = host + '/' + index + '/' + store_type
    r = requests.post(url, auth=awsauth, data=json.dumps(document), headers=headers)
    print(r.json())
    
    msg = "You have successfully created an Event " + event_name + "!"
    sendSNS(phone_number, msg)
    
    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        'body': json.dumps('Successfully Stored!!')
    }


def updateES(event_name, uni):
    print("in update")
            
    document = {
        "script" : {
            "inline": "ctx._source.RelatedUsers.add(params.user)",
            "params" : {
                "user" : uni
            }
        },
        "query": {
            "match_phrase": {
                "Name": event_name
            }
        }
    }
    
    print(document)
    
    url = host + '/' + index + '/' + update_type
    r = requests.post(url, auth=awsauth, data=json.dumps(document), headers=headers)
    print(r.json())
    
    return {
        'statusCode': 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        'body': json.dumps('Successfully Stored!!')
    }
    

# Lambda execution starts here
def lambda_handler(event, context):
    print (event)

    if "EventDate" in event.keys():
        print("In create events")
        event_name = event["EventName"].lower()
        event_date = event["EventDate"]
        event_time = event["EventTime"]
        event_location = event["EventLocation"]
        event_detail = event["EventDetails"]
        category = event["EventCategory"].lower()
        photo = event["EventPhoto"]
        creator = event["EventCreator"]
        phone_number = event["EventPhone"]
        
        storeToES(event_name, event_date, event_time, event_location, event_detail, category, photo, creator, phone_number)

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully Stored!')
        }

    elif "EventCategory" in event.keys():
        category = event["EventCategory"]
        events_found = queryFromES_category(category)
    
    else:
        try:
            user_ip = event["EventIP"]
        except:
            return ("IP Missing")
            
        uni, phone_number = queryFromDB(user_ip)
        if uni == "None":
            events_found = "You need to sign up first."
        else:
            if "EventName" in event.keys():
                event_name = event["EventName"].lower()
                events_found = updateES(event_name, uni)
                
                msg = "You have successfully added " + event_name + "to your account!"
                sendSNS(phone_number, msg)
            else:
                events_found = queryFromES_user(uni)

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        'body': json.dumps(events_found),
        "isBase64Encoded": False
    }

    return response