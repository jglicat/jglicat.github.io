import os
import shutil
import time
import matplotlib.pyplot as plt
base_path = 'C:/Program Files (x86)/Steam/steamapps/workshop/content/431960/'
dir_names = os.listdir(base_path)
count = 0
for dir_name in dir_names:
    try:
        img = plt.imread(base_path+dir_name+'/preview.jpg')
        plt.imshow(img)
        plt.pause(0.1)
        flag = input("是否保存此图片 y or n\n")
        if flag:
            shutil.copyfile(base_path+dir_name+'/preview.jpg', f"./{count}.jpg")
            count += 1
        # break
    except Exception as e:
        print(e)