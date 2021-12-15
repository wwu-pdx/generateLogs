import requests

import os
count = 0
url = 'http://us-central1-lognlp.cloudfunctions.net/pd5-f-access-243484628887'
#directory = r'G:\Face_dataset\original_images\original_images'
directory = r'original_images'
for entry in os.scandir(directory):
     if (entry.path.endswith(".jpg")
             or entry.path.endswith(".png")) and entry.is_file() and count<1:
         print(entry.path)
         files = {'media': open(entry.path, 'rb')}
         response=requests.post(url, files=files)
         count+=1
         print(response.content)
print(count)


