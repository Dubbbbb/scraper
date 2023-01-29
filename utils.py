import os

ID = -1

def get_id():
    global ID
    ID += 1
    return ID

def create_folder(folder_name):
    folder_path = os.getcwd() + folder_name
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)