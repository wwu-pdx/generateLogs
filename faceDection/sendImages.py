import requests
import os
import sys
count = 0

num = int(sys.argv[1]) #number of files want to use
if len(sys.argv) <3:
   url = 'https://us-central1-lognlp.cloudfunctions.net/pd5-f-access-713917766553'
else:
   url = sys.argv[2]
#directory = r'G:\Face_dataset\original_images\original_images'
headers={
'Referer' :'http://us-central1-lognlp.cloudfunctions.net/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
directory = r'original_images'
for entry in os.scandir(directory):
     if (entry.path.endswith(".jpg")
             or entry.path.endswith(".png")) and entry.is_file() and count<num:
         #print(entry.path)
         with open(entry.path, 'rb') as img:
            name_img= os.path.basename(entry.path)
            files= {'file': (name_img,img,'multipart/form-data',{'Expires': '0'}) } 
            response=requests.post(url, files=files,headers=headers)
            #print(response.status_code)
            #print(response.text)
         count+=1
         print(f'{count}  {print(name_img)}')
         




