import urllib2
import json


def lambda_handler(event, context):
    # TODO implement
    if event['request']['type'] == "IntentRequest":
        intent_name = extract_alexa_skill_name(event)
        print("Intent name = {}".format(intent_name))
        intent_slot = extract_alexa_slot_type(event)
        print("Intent Slot = {}".format(intent_slot))
        intent_slot_value = extract_alexa_skill_value(event, intent_slot)
        print("intent slot Value = {}".format(intent_slot_value))
        rhymes = find_rhymes(intent_slot_value)
    my_string = construct_string_from_list(rhymes)
    response = build_speechlet_response(title="",
                                        #output=','.join(rhymes),
                                        output=my_string,
                                        reprompt_text=None,
                                        should_end_session=True)
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


def find_rhymes(word):
    url = 'https://api.datamuse.com/words?rel_rhy='
    datamuse_retval = urllib2.urlopen('{}{}'.format(url, word)).read()
    json_rhymes = json.loads(datamuse_retval)
    rhymes = []
    for val in json_rhymes:
        rhymes.append(val['word'])
    return rhymes


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