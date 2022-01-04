from filelist import filelist
from google.cloud import storage
from googleapiclient import discovery
import google.auth
import sys
import random

filenames=filelist
num = int(sys.argv[1])

intervel = int(len(filenames)/num)
res = random.sample(range(1, intervel), num)

#storage_client = storage.Client()
storage_client = storage.Client.from_service_account_json('pd5-access.json')
buckets = storage_client.list_buckets()
bucketname=''
for bucket in buckets:
    if bucket.name.startswith( 'pd5-bucket-' ):
        bucketname= bucket.name
print(res)

