from filelist import filelist
from google.cloud import storage
from googleapiclient import discovery
import google.auth
import sys
import random

filenames=filelist
num = int(sys.argv[1])

intervel = int(len(filenames)/num)
waittime = [random.randrange(1, intervel, 1) for i in range(num)]
waittime.sort() 
chosenfiles= random.choices(filenames,k=num)
chosenfiles.sort()

#storage_client = storage.Client()
storage_client = storage.Client.from_service_account_json('pd5-access.json')
buckets = storage_client.list_buckets()
bucketname=''
for b in buckets:
    if b.name.startswith( 'pd5-bucket-' ):
        bucketname= b.name

# bucket = storage_client.bucket(bucketname)
# while len(chosenfiles)>0:
#     try:
#         blob = bucket.blob(chosenfiles[0])
#         blob.download_to_filename(chosenfiles[0])
#     except Exception as e:
#         print(str(e))



print(waittime)
print(chosenfiles)

