from cgitb import enable
from ctypes import sizeof
from turtle import right
import PySimpleGUI as sg
import os.path
import shutil
import pydicom as dicom
from pydicom import dcmread
import os 
import warnings
from tqdm import tqdm, trange

warnings.filterwarnings("ignore")


dest = 'C:./img/Insert_all_dcm_files_here'



def create(theme):
    sg.theme(theme)
    layout = [
        [
        sg.Text("Choose your Dicom folder"),
        sg.In(size=(30,5), enable_events = True, key = '-FOLDER-'),
        sg.FolderBrowse(key = '-IN-'),
        #sg.Button("MOVE"),
        sg.Button('Run', key = '-POPUP-')],
        [sg.Text('right click here', enable_events = True, key = '-EGG-', right_click_menu = theme_menu)        ]
    ]
    return sg.Window('Prenuvo', layout)

theme_menu = ['menu',['LightBrown9','DarkTeal7','DarkGrey1','BrightColors','DarkBlue14','LightBrown1','DarkBrown4','Reds','DarkPurple4','DarkPurple5','HotDogStand','random']]
# Create the window
window = create('DarkTeal7')
layoutpopup = [
            [sg.Text('Please Enter Patient, Date of Birth, ID, Name')],
            [sg.Text('Patient Date of Birth: MM-DD-YYYY', size=(26, 1)), sg.InputText( key='-DOB-')],
            [sg.Text('Patient ID', size=(26, 1)), sg.InputText( key='-ID-')],
            [sg.Text('Patient Name', size=(26, 1)), sg.InputText( key='-PNAME-')],
            [sg.Submit( key = '-PARTY-'), sg.Cancel()]
            ]
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    
    if event in theme_menu[1]:
        window.close()
        window = create(event)
        
    #if event == 'MOVE':
        #try:
         #   shutil.move(values['-IN-'], dest)
        #except:
         #   pass
    
    if event == '-POPUP-':
            try:
                shutil.move(values['-IN-'], dest)
            except:
                pass
            sg.theme('BrightColors')
            window = sg.Window('Data Entry Window', layoutpopup)
            event, values = window.read()
            window.close()

            ans0 = values['-DOB-']
            ans1 = values['-ID-']
            ans2 =  values['-PNAME-']

            #sg.Popup(event, values, ans0, ans1, ans2)
            if event == '-PARTY-':
                root = "./img/Insert_all_dcm_files_here/"
                padir = os.listdir(root)
                for i in range(0, len(padir)):
                    pa = padir[i]+"/"
                    sg.one_line_progress_meter(
                        'PA_Progress_Bar',
                        i + 1,
                        len(padir),
                        'PA Progress Bar',
                        root+pa,
                        orientation='h',
                        bar_color=('#F47264', '#FFFFFF')
                    )
                    stdir = os.listdir(root+pa)
                    for j in range(0, len(stdir)):
                        st = stdir[j]+"/"
                        sg.one_line_progress_meter(
							'ST_Progress_Bar',
							j + 1,
							len(stdir),
							'ST Progress Bar',
							root+pa+st,
							orientation='h',
							bar_color=('#F47264', '#FFFFFF')
						)
                        sedir = os.listdir(root+pa+st)
                        for n in range(0, len(sedir)):
                            se = sedir[n]+"/"
                            sg.one_line_progress_meter(
								'SE_Progress_Bar',
								n + 1,
								len(sedir),
								'SE Progress Bar',
								root+pa+st+se,
								orientation='h',
								bar_color=('#F47264', '#FFFFFF')
							)
                            pdir = os.listdir(root+pa+st+se)
                            for m in range(0, len(pdir)):
                                picture = pdir[m]
                                # sg.one_line_progress_meter(
								# 	'DICOM_PIC_Progress_Bar',
								# 	m + 1,
								# 	len(pdir),
								# 	'DICOM PIC Progress Bar',
								# 	root+pa+st+se+picture,
								# 	orientation='h',
								# 	bar_color=('#F47264', '#FFFFFF')
								# )
                                s = ""
                                if not picture.endswith('.dcm'):
                                    s = ".dcm"
                                os.rename(root+pa+st+se+picture,root+pa+st+se+picture+s)
                                f = dicom.read_file(root+pa+st+se+picture+s)
                                tag0 = 'PatientBirthDate'
                                if tag0 in f:
                                    f.data_element(tag0).value = ans0

                                tag1 = 'PatientID'
                                if tag1 in f:
                                    f.data_element(tag1).value = ans1

                                tag2 = 'PatientName'
                                if tag2 in f:
                                    f.data_element(tag2).value = ans2
                                f.save_as(root+pa+st+se+picture+s)
       
window.close()