import azure.cognitiveservices.speech as speechsdk
import json
import requests

def Read(Subscription,Region,lang,win_con):
    #the default language is English, so flag should be defaultly set to 0

    print("Say something...")
    if lang == 'English':
        print("Detecting English")
    else:
        print("正在接收中文")

    """performs one-shot intent recognition from input from the default microphone"""
    # <IntentRecognitionOnceWithMic>
    # Set up the config for the intent recognizer (remember that this uses the Language Understanding key, not the Speech Services key)!

    if lang == "English":
        Subscription = "c0fecdc679a84400a8bb4b914ab624ea"
    else:
        Subscription = "4292ba575c2c4a60b4868f2f3f308668"

    intent_config = speechsdk.SpeechConfig(subscription=Subscription, region=Region)

    # Set up the intent recognizer
    if lang == 'English':
        intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=intent_config)
    else:
        intent_recognizer = speechsdk.SpeechRecognizer(speech_config=intent_config,language="zh-CN")
    # set up the intents that are to be recognized. These can be a mix of simple phrases and
    # intents specified through a LanguageUnderstanding Model.


    intent_result = intent_recognizer.recognize_once()

# Check the results
    if intent_result.reason == speechsdk.ResultReason.RecognizedIntent:
        print("Recognized: \"{}\" with intent id `{}`".format(intent_result.text, intent_result.intent_id))
    elif intent_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(intent_result.text))
        if lang == 'English':
            endpointUrl = 'https://language-hht.cognitiveservices.azure.com/luis/prediction/v3.0/apps/4bd8fe50-b52e-475d-a529-a772b3c6157f/slots/production/predict?subscription-key=c0fecdc679a84400a8bb4b914ab624ea&verbose=true&show-all-intents=true&log=true&query='
        else:
            endpointUrl = 'https://language-hht.cognitiveservices.azure.com/luis/prediction/v3.0/apps/81745a54-6cef-4dee-8a5a-3dea8fc56dc1/slots/production/predict?subscription-key=c0fecdc679a84400a8bb4b914ab624ea&verbose=true&show-all-intents=true&log=true&query='



        endpoint = endpointUrl + intent_result.text
        response = requests.get(endpoint)
        data = response.json()

        intent = data['prediction']['topIntent']
        entity = data['prediction']['entities']





        result = Judement(intent,entity,lang)


    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(intent_result.no_match_details))
    elif intent_result.reason == speechsdk.ResultReason.Canceled:
        print("Intent recognition canceled: {}".format(intent_result.cancellation_details.reason))
        if intent_result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(intent_result.cancellation_details.error_details))



    return result
#    return intent_result.reason

# </IntentRecognitionOnceWithMic>


#Judement Function is to return the
#
def Judement(intent, entity,lang):
    if (intent == "All On"):
        if lang == "English":
            if(entity['color'] == ['green']):
                judement_result = "AllGreen"
            else:
                judement_result = "AllOn"
        else:
            if(entity['颜色'] == ['绿色']):
                judement_result = "AllGreen"
            else:
                judement_result = "AllOn"
    elif (intent == "All Off"):
        judement_result = "AllOff"
    elif (intent == "Light On"):
        if lang == "English":
            if (entity['color'] == ['green']):
                if(entity['location'] == ['on the desk'] or entity['location'] == ['on the left']):
                    judement_result = "DeskGreen"
                elif (entity['location'] == ['on the right'] or entity['location'] == ['on the floor']):
                    judement_result = "FloorGreen"
            else:
                if(entity['location'] == ['on the desk'] or entity['location'] == ['on the left']):
                    judement_result = "DeskOn"
                elif (entity['location'] == ['on the right'] or entity['location'] == ['on the floor']):
                    judement_result = "FloorOn"
        else:
            if (entity['颜色'] == ['绿色']):
                if (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台']):
                    judement_result = "DeskGreen"
                elif (entity['位置'] == ['右边'] or entity['位置'] == ['地上'] or entity['位置'] == ['地板上']):
                    judement_result = "FloorGreen"
            else:
                if (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台']):
                    judement_result = "DeskOn"
                elif (entity['位置'] == ['右边'] or entity['位置'] == ['地上'] or entity['位置'] == ['地板上']):
                    judement_result = "FloorOn"
    elif (intent == "Light Off"):
        if lang == "English":
            if(entity['location'] == ['on the desk'] or entity['location'] == ['on the left']):
                judement_result = "DeskOff"
            elif (entity['location'] == ['on the right'] or entity['location'] == ['on the floor']):
                judement_result = "FloorOff"
        else:
            if (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台']):
                judement_result = "DeskOff"
            elif (entity['位置'] == ['右边'] or entity['位置'] == ['地上'] or entity['位置'] == ['地板上']):
                judement_result = "FloorOff"
    elif (intent == "None"):
        judement_result = "end"

    return judement_result


