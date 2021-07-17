import PySimpleGUI as sg
import sys
import os
import LUIS_quickstart
import azure.cognitiveservices.speech as speechsdk
#import congnitive_quickstart
import requests
import json

program_path = os.getcwd()
cache_path = program_path+r'\cache' # 缓存文件路径

sg.theme('DarkBlue')

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

        if (intent == "AC On" ):
            if (intent == "AC On"):
                if (win_con['-On-'].get() == False):
                    win_con['-On-'].update(value=True)
                    win_con['-Temp-'].update(f"25")
                    win_con['-Temp-Slider-'].update('25')
                    win_con['-Hum-'].update(f'50')
                    win_con['-Hum-Slider-'].update('50')
                if ("AcOn" in entity or "temperature" in entity):
                    temper = entity['number'][0]

                    win_con['-Temp-'].update(temper)
                    win_con['-Temp-Slider-'].update(temper)
                elif ("Humidity" in entity or "percentage" in entity):
                    humi = entity['number'][0]
                    win_con['-Hum-'].update(humi)
                    win_con['-Hum-Slider-'].update(humi)
                result = "AC"
        elif (intent == "AC Up"):
            if "Humidity" in entity:
                Orin_Humi = int(win_con['-Hum-'].get())
                Raise_Humi = entity['number'][0]
                Curr_Humi = Orin_Humi + Raise_Humi
                win_con['-Hum-'].update(Curr_Humi)
                win_con['-Hum-Slider-'].update(Curr_Humi)
                result = "AC"
            else:
                Orin_Temp = int(win_con['-Temp-'].get())
                Raise_Temp = entity['number'][0]
                Curr_Temp = Orin_Temp + Raise_Temp
                win_con['-Temp-'].update(Curr_Temp)
                win_con['-Temp-'].update(Curr_Temp)
                result = "AC"
        elif intent == "AC Down":
            if "Humidity" in entity:
                Orin_Humi = int(win_con['-Hum-'].get())
                Raise_Humi = entity['number'][0]
                Curr_Humi = Orin_Humi - Raise_Humi
                win_con['-Hum-'].update(Curr_Humi)
                win_con['-Hum-Slider-'].update(Curr_Humi)
                result = "AC"
            else:
                Orin_Temp = int(win_con['-Temp-'].get())
                Raise_Temp = entity['number'][0]
                Curr_Temp = Orin_Temp - Raise_Temp
                win_con['-Temp-'].update(Curr_Temp)
                win_con['-Temp-Slider-'].update(Curr_Temp)
                result = "AC"
        elif (intent == "AC Off"):
            win_con['-Off-'].update(value=True)
            win_con['-On-'].update(value=False)
            win_con['-Temp-'].update("")
            win_con['-Temp-Slider-'].update("10")
            win_con['-Hum-'].update("")
            win_con['-Hum-Slider-'].update("0")
            result = "AC"
        else:
            result = Judement(intent,entity,lang)






    elif intent_result.reason == speechsdk.ResultReason.NoMatch:
        result = "No_Match"
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





def main_gui(): # 程序主界面
    if os.path.exists(cache_path) == False:
        os.makedirs(cache_path)


    layout = [[sg.Text('欢迎使用StoU')],
              [sg.Text('Subscription'),sg.Text('Default_Value: c0fecdc679a84400a8bb4b914ab624ea')],
              [sg.InputText(default_text = 'c0fecdc679a84400a8bb4b914ab624ea', key = '-Sub-')],
              [sg.Text('ServiceRegion'),sg.Text('Default_Value: westus')],
              [sg.InputText(default_text= 'westus' ,key = '-Region-')],
              [sg.Button('开始识别')],
              [sg.Button('退出程序')]
              ]

    win_main = sg.Window('StoU语义理解', layout,font=("宋体", 15),size=(600,300))



    event, values = win_main.read()

    Subscription = values['-Sub-']
    ServiceRegion = values['-Region-']


    """Set a boolean variable named flag to indicate if the language is English or Simplified Chinese"""


    if event in (None, '退出程序'):
        win_main.close()
    elif event == '开始识别':
        Con_gui(win_main,Subscription,ServiceRegion)

    win_main.close()

def Update_Image(result,win_con,cwd):
    if result == 'AllOn':
        filename_Desk = cwd + '/image/desk-yellow.png'
        filename_Floor = cwd + '/image/floor-yellow.png'
        win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
        win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    elif result =="AllOff":
        filename_Desk = cwd +'/image/desk-off.png'
        filename_Floor = cwd + '/image/floor-off.png'
        win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
        win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    elif result =="DeskOn":
        filename_Desk = cwd + '/image/desk-yellow.png'
        win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
    elif result == "DeskOff":
        filename_Desk = cwd + '/image/desk-off.png'
        win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
    elif result == "FloorOn":
        filename_Floor = cwd + '/image/floor-yellow.png'
        win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    elif result == "FloorOff":
        filename_Floor = cwd + '/image/floor-off.png'
        win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    elif result == "AllGreen":
        filename_Desk = cwd + '/image/desk-green.png'
        filename_Floor = cwd + '/image/floor-green.png'
        win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
        win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    elif result == "DeskGreen":
        filename_Desk = cwd + '/image/desk-green.png'
        win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
    elif result == "FloorGreen":
        filename_Floor = cwd + '/image/floor-green.png'
        win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))



def Con_gui(win_main,Subscription,ServiceRegion):
    win_main.Hide()

    left_col = [
        [sg.Button('开始识别'),sg.Button('退出')],[sg.Text('Language_Select'),sg.Combo(['简体中文','English'],default_value='English',key = '-Lang-')],
        [sg.Text('Output')],
        [sg.Output(size=(30,20))] #到时候还要放Image
    ]

    images_col = [
        [sg.Text('The image recognized')],
        [sg.Image(key='-Desk-'),sg.Image(key='-Floor-')]
    ]

    AC_col = [
        [sg.Text("Air Condition")],
        [sg.Radio("On","RADIO1",key= '-On-'),sg.Radio("Off","RADIO1",default=True,key='-Off-')],
        [],
        [sg.Text("Temperature(Celsius Degree)/温度(摄氏度)",size=(40,2)),sg.Text(key='-Temp-',size=(20,2))],
        [],
        [sg.Text("Temperature Visualizer"),sg.Slider((10,40),key='-Temp-Slider-',enable_events=True,orientation='h')],
        [],
        [sg.Text("Humidity(%)/湿度(%)",size=(40,2)),sg.Text(key='-Hum-',size=(20,2))],
        [],
        [sg.Text("Humidity Visualizer"),sg.Slider((0,100),key='-Hum-Slider-',enable_events=True,orientation='h')]
    ]

    layout_Con =[[sg.Column(left_col,element_justification='c'),sg.Column(images_col,element_justification='c'),sg.Column(AC_col,justification='c')]]

    cwd = os.getcwd()
    filename_Desk = cwd + '/image/desk-off.png'
    filename_Floor = cwd + '/image/floor-off.png'

    win_con = sg.Window('StoU语义理解',layout_Con,font = ("宋体",15),size = (1500,500),finalize=True)



#    win_con.Read()

    win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
    win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    """While Loop here is for recognizing more than once, but may be improved in the following development"""
    while True:
        con_event, con_values = win_con.Read()
        lang = con_values['-Lang-']
        if con_event == '开始识别':
            while True:
                result = Read(Subscription,ServiceRegion,lang,win_con)
                if result == "end" :
                    if lang == "English":
                        print("Stop Detecting")
                    else:
                        print("停止识别")
                    break
                elif result == "No_Match":
                    continue
                else:
                    Update_Image(result,win_con,cwd)

        if con_event in (None,'退出'):
            break
    win_con.close()


def main():
    main_gui()

if __name__ == '__main__':
    main()

