import json
import boto3

client = boto3.client('sqs')

"""
This sample demonstrates an implementation of the Lex Code Hook Interface
in order to serve a sample bot which manages orders for flowers.
Bot, Intent, and Slot models which are compatible with this sample can be found in the Lex Console
as part of the 'OrderFlowers' template.

For instructions on how to set up and test this bot, as well as additional samples,
visit the Lex Getting Started documentation http://docs.aws.amazon.com/lex/latest/dg/getting-started.html.
"""
import math
import dateutil.parser
import datetime
import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


""" --- Helpers to build responses which match the structure of the necessary dialog actions --- """


def get_slots(intent_request):
    return intent_request['currentIntent']['slots']


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


""" --- Helper Functions --- """


def parse_int(n):
    try:
        return int(n)
    except ValueError:
        return float('nan')


def build_validation_result(is_valid, violated_slot, message_content):
    if message_content is None:
        return {
            "isValid": is_valid,
            "violatedSlot": violated_slot,
        }

    return {
        'isValid': is_valid,
        'violatedSlot': violated_slot,
        'message': {'contentType': 'PlainText', 'content': message_content}
    }


def isvalid_date(date):
    try:
        dateutil.parser.parse(date)
        return True
    except ValueError:
        return False


def validate_search_events(category, event_date, event_time, phone_number):
    categories = ['official', 'individual', 'organization']
    
    if category is not None and category.lower() not in categories:
        return build_validation_result(False,
                                       'Category',
                                       'We do not have {}, would you like a different category?  '
                                       'Our most popular categories are {}'.format(category, categories))

    if event_date is not None:
        if not isvalid_date(event_date):
            return build_validation_result(False, 'EventDate', 'I did not understand that, what day would you like to searh?')
        elif datetime.datetime.strptime(event_date, '%Y-%m-%d').date() < datetime.date.today():
            return build_validation_result(False, 'EventDate', 'You cannot search for past dates. What day would you like to search?')
       
    if event_time is not None:
        if len(event_time) != 5:
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'EventTime', 'The event time input is invalid.')

        hour, minute = event_time.split(':')
        hour = parse_int(hour)
        minute = parse_int(minute)
        if math.isnan(hour) or math.isnan(minute):
            # Not a valid time; use a prompt defined on the build-time model.
            return build_validation_result(False, 'EventTime', 'The event time input is invalid.')
    
    if phone_number is not None:
        if len(phone_number) != 10:
            return build_validation_result(False, 'PhoneNumber', 'The phone number is invalid.')
        
    return build_validation_result(True, None, None)


""" --- Functions that control the bot's behavior --- """

def search_resteraunts(intent_request):
    """
    Performs dialog management and fulfillment for ordering flowers.
    Beyond fulfillment, the implementation of this intent demonstrates the use of the elicitSlot dialog action
    in slot validation and re-prompting.
    """
    category = get_slots(intent_request)["Category"]
    event_date = get_slots(intent_request)["EventDate"]
    event_time = get_slots(intent_request)["EventTime"]
    phone_number = get_slots(intent_request)["PhoneNumber"]
    
    intent = intent_request['currentIntent']
    source = intent_request['invocationSource']
    
    if source == 'DialogCodeHook':
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt for the first violation detected.
        slots = get_slots(intent_request)

        validation_result = validate_search_events(category, event_date, event_time, phone_number)
        if not validation_result['isValid']:
            slots[validation_result['violatedSlot']] = None
            return elicit_slot(intent_request['sessionAttributes'],
                               intent_request['currentIntent']['name'],
                               slots,
                               validation_result['violatedSlot'],
                               validation_result['message'])

        # Pass the price of the flowers back through session attributes to be used in various prompts defined
        # on the bot model.
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}

        return delegate(output_session_attributes, get_slots(intent_request))

    # Search the Restaurants, and rely on the goodbye message of the bot to define the message to the end user.
    # In a real bot, this would likely involve a call to a backend service.
    return close(intent_request['sessionAttributes'],
                 'Fulfilled',
                 {'contentType': 'PlainText',
                  'content': 'Okay, we have received your request and we will notify you over SMS once you have the list of restaurant suggestions.'})

""" --- Intents --- """


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'EventRec':
        return search_resteraunts(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


""" --- Main handler --- """


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    # logger.debug('event.bot.name={}'.format(event['bot']['name']))

    val = dispatch(event)
    if val['dialogAction']['type'] != 'Close':
        slots = val['dialogAction']['slots']
        intent = event['currentIntent']['name']

        hasNull = 0
        for slot in slots.values():
            if slot is None:
                hasNull = 1

        if hasNull == 0 and intent == 'EventRec':
            result = json.dumps(slots)
            print(result)
            response = client.send_message(
                QueueUrl='',
                MessageBody= result
            )
    return val