import azure.cognitiveservices.speech as speechsdk
import json
import requests


# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
#speech_key, service_region = "YourSubscriptionKey", "YourServiceRegion"
#speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)



def Read(Subscription,Region,lang):
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

#    if lang == 'English':
#        APPID = "4bd8fe50-b52e-475d-a529-a772b3c6157f"
#    else:
#        APPID = "81745a54-6cef-4dee-8a5a-3dea8fc56dc1"

#    model = speechsdk.intent.LanguageUnderstandingModel(app_id=APPID)
#    intents = [
#        (model, "HA_2.AllOFF"),
#        (model, "HA_2.AllON"),
#        (model, "Color"),
#        (model, "LightOff"),
#        (model, "LightOn")
#    ]
    #intent_recognizer.add_intents(intents)

# Starts intent recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed. It returns the recognition text as result.
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query.
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.

#    endpointUrl = 'https://hht-luis.cognitiveservices.azure.com/luis/prediction/v3.0/apps/5df4ce63-7d39-4fa4-acbd-e2eec3191005/slots/production/predict?subscription-key=7623c4ad5edd43daae3a5687e4d690e7&verbose=true&show-all-intents=true&log=true&query='
    #if flag == 1:
     #   translation.translation_once_from_mic(Subscription,Region,flag)
#    endpoint = endpointUrl + intent_result.text
#    response = requests.get(endpoint)
#    data = response.json()

#    intent = data['prediction']["topIntent"]
#    if (intent == "All ON"):
#        print("Recognized: \"{}\" ".format(intent_result.text))
#        result = "AllOn"


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

        if lang == 'English':
            result = Judement_English(intent,entity)
        else:
            result = Judement_Chinese(intent,entity)


    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(intent_result.no_match_details))
    elif intent_result.reason == speechsdk.ResultReason.Canceled:
        print("Intent recognition canceled: {}".format(intent_result.cancellation_details.reason))
        if intent_result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(intent_result.cancellation_details.error_details))

    if intent_result.reason == speechsdk.ResultReason.NoMatch:
        result = 'End'

    return result
#    return intent_result.reason

# </IntentRecognitionOnceWithMic>

def Judement_English(intent, entity):
    if (intent == "All On"):
        judement_result = "AllOn"
    elif (intent == "All Off"):
        judement_result = "AllOff"
    elif (intent == "Light On" and (entity['location'] == ['on the desk'] or entity['location'] == ['on the left'])):
        judement_result = "DeskOn"
    elif (intent == "Light Off" and (entity['location'] == ['on the desk'] or entity['location'] == ['on the left'])):
        judement_result = "DeskOff"
    elif (intent == "Light On" and (entity['location'] == ['on the right'] or entity['location'] == ['on the floor'])):
        judement_result = "FloorOn"
    elif (intent == "Light Off" and (entity['location'] == ['on the floor'] or entity['location'] == ['on the right'])):
        judement_result = "FloorOff"
    elif (intent == "All Color" and  entity['color'] == ['green']):
        judement_result = "AllGreen"
    elif (intent == "All Color" and  entity['color'] == ['yellow']):
        judement_result = "AllYellow"
    elif (intent == "Change Color" and (entity['location'] == ['on the desk'] or entity['location'] == ['on the left']) and entity['color'] == ['green']):
        judement_result = "DeskGreen"
    elif (intent == "Change Color" and (entity['location'] == ['on the right'] or entity['location'] == ['on the floor']) and entity['color' == ['green']]):
        judement_result = "FloorGreen"
    elif (intent == "Change Color" and (entity['location'] == ['on the desk'] or entity['location'] == ['on the left']) and entity['color'] == ['yellow']):
        judement_result = "DeskYellow"
    elif (intent == "Change Color" and (entity['location'] == ['on the right'] or entity['location'] == ['on the floor']) and entity['color'] == ['yellow']):
        judement_result = "FloorYellow"

    return judement_result


def Judement_Chinese(intent, entity):
    if (intent == "全开"):
        judment_result = "AllOn"
    elif (intent == "全关"):
        judment_result = "AllOff"
    elif (intent == "开灯" and (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台'])):
        judment_result = "DeskOn"
    elif (intent == "关灯" and (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台'])):
        judment_result = 'DeskOff'
    elif (intent == "开灯" and (entity['位置'] == ['右边'] or entity['位置'] == ['地上'] or entity['位置'] == ['地上'])):
        judment_result = "FloorOn"
    elif (intent == "关灯" and (entity['位置'] == ['右边'] or entity['位置'] == ['地板上'] or entity['位置'] == ['地上'])):
        judment_result = 'FloorOff'
    elif (intent == '全部变颜色' and entity['颜色'] == ['绿色']):
        judment_result = 'AllGreen'
    elif (intent == '全部变颜色' and entity['颜色'] == ['黄色']):
        judment_result = "AllYellow"
    elif (intent == '变颜色' and (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台']) and entity['颜色'] == ['绿色']):
        judment_result = "DeskGreen"
    elif (intent == '变颜色' and (entity['位置'] == ['右边'] or entity['位置'] == ['地上'] or entity['位置'] == ['地板上']) and entity['颜色'] == ['绿色']):
        judment_result = "FloorGreen"
    elif (intent == '变颜色' and (entity['位置'] == ['左边'] or entity['位置'] == ['桌子上'] or entity['位置'] == ['台']) and entity['颜色'] == ['黄色']):
        judment_result = "DeskYellow"
    elif (intent == '变颜色' and (entity['位置'] == ['右边'] or entity['位置'] == ['地上'] or entity['位置'] == ['地板上']) and entity['颜色'] == ['黄色']):
        judment_result = "FloorYellow"


    return judment_result