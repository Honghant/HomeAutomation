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

    layout_Con =[[sg.Column(left_col,element_justification='c'),sg.Column(images_col,element_justification='c')]]

    cwd = os.getcwd()
    filename_Desk = cwd + '/image/desk-off.png'
    filename_Floor = cwd + '/image/floor-off.png'

    win_con = sg.Window('StoU语义理解',layout_Con,font = ("宋体",15),size = (1000,500),finalize=True)



#    win_con.Read()

    win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
    win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
    """While Loop here is for recognizing more than once, but may be improved in the following development"""
    while True:
        con_event, con_values = win_con.Read()
        lang = con_values['-Lang-']
        if con_event == '开始识别':
            while True:
                result = congnitive_quickstart.Read(Subscription,ServiceRegion,lang)
                if result == "End" or result == "No_Match":
                    break
                elif result == 'AllOn':
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
                elif result == "AllYellow":
                    filename_Desk = cwd + '/image/desk-yellow.png'
                    filename_Floor = cwd + '/image/floor-yellow.png'
                    win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
                    win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
                elif result == "DeskGreen":
                    filename_Desk = cwd + '/image/desk-green.png'
                    win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
                elif result == "FloorGreen":
                    filename_Floor = cwd + '/image/floor-green.png'
                    win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))
                elif result == "DeskYellow":
                    filename_Desk = cwd + '/image/desk-yellow.png'
                    win_con['-Desk-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Desk))
                elif result == "FloorYellow":
                    filename_Floor = cwd + '/image/floor-yellow.png'
                    win_con['-Floor-'].update(data=LUIS_quickstart.convert_to_bytes(filename_Floor))




        if con_event in (None,'退出'):
            break
    win_con.close()


def main():
    main_gui()

if __name__ == '__main__':
    main()
