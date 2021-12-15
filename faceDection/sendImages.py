import requests

import os
count = 0
url = 'http://us-central1-lognlp.cloudfunctions.net/pd5-f-access-435635627182'
#directory = r'G:\Face_dataset\original_images\original_images'
headers={
'Referer' :'http://us-central1-lognlp.cloudfunctions.net/',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
directory = r'original_images'
for entry in os.scandir(directory):
     if (entry.path.endswith(".jpg")
             or entry.path.endswith(".png")) and entry.is_file() and count<1000:
         print(entry.path)
         with open(entry.path, 'rb') as img:
            name_img= os.path.basename(entry.path)
            files= {'file': (name_img,img,'multipart/form-data',{'Expires': '0'}) } 
            response=requests.post(url, files=files,headers=headers)
            print(response.status_code)
            #print(response.text)
         count+=1
         
print(count)


