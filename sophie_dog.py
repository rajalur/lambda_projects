import urllib2
import json

counter = 0

def lambda_handler(event, context):

    global counter
    
    if event['request']['type'] == "LaunchRequest":
        game_state = "STARTED"
        counter = 0        
        my_string = "Play a word"
        response = build_speechlet_response(title="",
                                        output=my_string,
                                        reprompt_text=None,
                                        should_end_session=False)
        return build_response({}, response)
    elif event['request']['type'] == "IntentRequest":
        intent_name = extract_alexa_skill_name(event)
        if intent_name == "AMAZON.CancelIntent" or intent_name =="AMAZON.StopIntent":
            out_string = "Goodbye"
            session_state = "True"

        else:
            intent_slot = extract_alexa_slot_type(event)
            intent_slot_value = extract_alexa_skill_value(event, intent_slot)
            counter += 1
            out_string = "Sophie says, you said "+intent_slot_value + "      "+ " And  My counter is {}".format(counter)
            session_state = "False"
            
    response = build_speechlet_response(title="",
                                      output=out_string,
                                       reprompt_text=None,
                                       should_end_session=session_state)
    return build_response({}, response)


def construct_string_from_list(my_list):
    my_string = ''
    for l in my_list:
        my_string += l
        my_string += ','
    return my_string[:-1]

def extract_alexa_skill_name(json_input_to_lambda):
    return json_input_to_lambda['request']['intent']['name']


def extract_alexa_slot_type(json_input_to_lambda):
    for key in json_input_to_lambda['request']['intent']['slots'].keys():
        if 'name' in json_input_to_lambda['request']['intent']['slots'][key].keys():
            return key
    return ''


def extract_alexa_skill_value(json_input_to_lambda, slot_type):
    return json_input_to_lambda['request']['intent']['slots'][slot_type]['value']



def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
