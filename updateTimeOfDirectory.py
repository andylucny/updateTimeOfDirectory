import os
import time
import PySimpleGUI as sg

# GUI layout
layout = [
    [sg.Text('Select a directory:')],
    [sg.Input(key='-FOLDER-', enable_events=True), sg.FolderBrowse()],
    [sg.Button('Update', key='-UPDATE-', disabled=True)],
    [sg.Output(size=(80, 10))]
]

window = sg.Window('Update Time Of Directory', layout)

def update_directory_creation_dates(directory):
    dates = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if not os.path.isdir(item_path):
            dates.append(os.path.getmtime(item_path))
        else:
            if update_directory_creation_dates(item_path):
                dates.append(os.path.getmtime(item_path))
            
    if len(dates) > 0:
        newest_file_mtime = max(dates)
        # Update directory creation date
        os.utime(directory, (newest_file_mtime, newest_file_mtime))
        print(f"{directory} -> {time.ctime(newest_file_mtime)}")
        window.read(timeout=0.1)
        return True
    return False

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-FOLDER-':
        folder_path = values['-FOLDER-']
        if folder_path:
            window['-UPDATE-'].update(disabled=False)
        else:
            window['-UPDATE-'].update(disabled=True)
    elif event == '-UPDATE-':
        folder_path = values['-FOLDER-']
        update_directory_creation_dates(folder_path)
        print("Updated.")

window.close()
