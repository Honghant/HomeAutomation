
#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.
"""
Translation recognition samples for the Microsoft Cognitive Services Speech SDK
"""

import time
import os
import azure.cognitiveservices.speech as speechsdk

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    print("""
    Importing the Speech SDK for Python failed.
    Refer to
    https://docs.microsoft.com/azure/cognitive-services/speech-service/quickstart-python for
    installation instructions.
    """)
    import sys
    sys.exit(1)







def translation_once_from_mic(Subscription,Region,flag):
    """performs one-shot speech translation from input from an audio file"""
    # <TranslationOnceWithMic>
    # set up translation parameters: source language and target languages

    print("Say something...")
    print("Detecting 简体中文")


    # Potential mistakes: the speech_key here is the Key for Speech(Azure)
    # But Subscription passed in is the Key for LUIS App
    # So I first comment both of them

    # speech_key = Subscription
    # service_region = Region

    # There is a branch before, only flag is 1, this function will be called

    #from_language = 'en-US'
    #to_language = 'en-US'

    if flag == 1:
        from_language = 'zh-Hans'
        to_language = 'en-US'


    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=
        'ccced91cdceb4a2898849f46ae184815', region='eastasia',
        speech_recognition_language=from_language,
        target_languages=('en-US','dr')
    )
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    # Starts translation, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognized text as well as the translation.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    result = recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("""Recognized: {}
        English translation: {}""".format(
            result.text,
            result.translations['en-US']))
    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Translation canceled: {}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(result.cancellation_details.error_details))
    # </TranslationOnceWithMic>




