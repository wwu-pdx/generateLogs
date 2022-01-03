import requests
import sys
import os
filenames= []
count = 0
num = int(sys.argv[1]) #number of files want to use
#directory = r'G:\Face_dataset\original_images\original_images'

directory = r'original_images'
for entry in os.scandir(directory):
     if (entry.path.endswith(".jpg")
             or entry.path.endswith(".png")) and entry.is_file() and count<num:
         #print(entry.path)
         with open(entry.path, 'rb') as img:
            name_img= os.path.basename(entry.path)
            filenames.append(name_img)
            print(name_img)
            #response=requests.post(url, files=files,headers=headers)
            #print(response.status_code)
            #print(response.text)
         count+=1
         
print(count)
#print(filenames)
f = open("filelist.py", "w")
f.write(f'filelist={filenames}')
f.close()

