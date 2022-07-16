import os
path = r'C:\Users\shibi\PycharmProjects\Mini_Project_G9\shots'
file_list = os.listdir(path)

for fnames in file_list:
    os.remove(path + '\\' + fnames)