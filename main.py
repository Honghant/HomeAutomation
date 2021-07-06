import PySimpleGUI as sg
import sys
import os
import LUIS_quickstart
import azure.cognitiveservices.speech as speechsdk
import congnitive_quickstart
import requests
import json

program_path = os.getcwd()
cache_path = program_path+r'\cache' # 缓存文件路径

sg.theme('DarkBlue')


def main_gui(): # 程序主界面
    if os.path.exists(cache_path) == False:
        os.makedirs(cache_path)


    layout = [[sg.Text('欢迎使用StoU')],
              [sg.Text('Subscription'),sg.Text('Default_Value: 7623c4ad5edd43daae3a5687e4d690e7')],
              [sg.InputText(default_text = '7623c4ad5edd43daae3a5687e4d690e7', key = '-Sub-')],
              [sg.Text('ServiceRegion'),sg.Text('Default_Value: westus')],
              [sg.InputText(default_text= 'westus' ,key = '-Region-')],
              [sg.Text('Language_Select'),sg.Combo(['简体中文','English'],default_value='English',key = '-Lang-')],
              [sg.Button('开始识别')],
              [sg.Button('退出程序')]
              ]

    win_main = sg.Window('StoU语义理解', layout,font=("宋体", 15),size=(600,300))



    event, values = win_main.read()

    Subscription = values['-Sub-']
    ServiceRegion = values['-Region-']
    Language = values['-Lang-']

    """Set a boolean variable named flag to indicate if the language is English or Simplified Chinese"""
    if Language == "English":
        flag = 0
    else:
        flag = 1

    if event in (None, '退出程序'):
        win_main.close()
    elif event == '开始识别':
        Con_gui(win_main,Subscription,ServiceRegion,flag)

    win_main.close()


def Con_gui(win_main,Subscription,ServiceRegion,flag):
    win_main.Hide()



    left_col = [
        [sg.Button('开始识别'),sg.Button('退出')],
        [sg.Text('Output')],[sg.Text('The image recognized')],
        [sg.Output(size=(30,20))] #到时候还要放Image
    ]

    images_col = [
       [sg.Image(key='-Desk-'),sg.Image(key='-Floor-')]
    ]

    layout_Con =[[sg.Column(left_col,element_justification='c'),sg.Column(images_col,element_justification='c')]]

    cwd = os.getcwd()
    filename = cwd + '/image/desk-off.png'

    win_con = sg.Window('StoU语义理解',layout_Con,font = ("宋体",15),size = (800,500))

#    win_con.Read()
    win_con['-Image-'].update(data=LUIS_quickstart.convert_to_bytes(filename))

    """While Loop here is for recognizing more than once, but may be improved in the following development"""
    while True:
        con_event, con_values = win_con.Read()

        if con_event == '开始识别':
            while True:

                result = congnitive_quickstart.Read(Subscription,ServiceRegion,flag)

                if result == speechsdk.ResultReason.NoMatch:
                    break
        if con_event in (None,'退出'):
            break
    win_con.close()


def main():
    main_gui()

if __name__ == '__main__':
    main()
