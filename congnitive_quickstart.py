import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
#speech_key, service_region = "YourSubscriptionKey", "YourServiceRegion"
#speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Creates a recognizer with the given settings
# speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)



def Read(Subscription,Region,flag = 0):
    #the default language is English, so flag should be defaultly set to 0

    print("Say something...")
    print("Detecting English")

    """performs one-shot intent recognition from input from the default microphone"""
    # <IntentRecognitionOnceWithMic>
    # Set up the config for the intent recognizer (remember that this uses the Language Understanding key, not the Speech Services key)!
    intent_config = speechsdk.SpeechConfig(subscription=Subscription, region=Region)

    # Set up the intent recognizer
    intent_recognizer = speechsdk.intent.IntentRecognizer(speech_config=intent_config)

    # set up the intents that are to be recognized. These can be a mix of simple phrases and
    # intents specified through a LanguageUnderstanding Model.
    model = speechsdk.intent.LanguageUnderstandingModel(app_id="5df4ce63-7d39-4fa4-acbd-e2eec3191005")
    intents = [
        (model, "HomeAutomation.TurnOn"),
        (model, "HomeAutomation.TurnOff")
    ]
    intent_recognizer.add_intents(intents)

# Starts intent recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed. It returns the recognition text as result.
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query.
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    intent_result = intent_recognizer.recognize_once()

    #if flag == 1:
     #   translation.translation_once_from_mic(Subscription,Region,flag)

# Check the results
    if intent_result.reason == speechsdk.ResultReason.RecognizedIntent:
        print("Recognized: \"{}\" with intent id `{}`".format(intent_result.text, intent_result.intent_id))
    elif intent_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(intent_result.text))
    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(intent_result.no_match_details))
    elif intent_result.reason == speechsdk.ResultReason.Canceled:
        print("Intent recognition canceled: {}".format(intent_result.cancellation_details.reason))
        if intent_result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(intent_result.cancellation_details.error_details))

#    if intent_result.reason == speechsdk.ResultReason.NoMatch:
#        result = 'No_Match'
#        return result
#    else:
#        return
    return intent_result.reason

# </IntentRecognitionOnceWithMic>

