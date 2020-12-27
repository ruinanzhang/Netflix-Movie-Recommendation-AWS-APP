import boto3
import botocore
import json
import random

BUCKET_NAME = 'cc-final-proj' 
KEY = '/tmp/data_part2_test.txt'
LOCAL_FILE = '/tmp/data_part2_test.txt'
s3 = boto3.resource('s3')
try:
    obj=s3.Bucket(BUCKET_NAME).download_file(LOCAL_FILE,KEY)
    print("Found obj file")
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
    else:
        print("Other errors")
with open('/tmp/data_part2_test.txt', 'a') as fd:
    uid = 5001
    print("open file ok")
    for i in range(5):
        mid = random.randint(1,26) # movie in range in the rating dataset
        rating = random.randint(1,5)
        string = str(mid) + "\t" + str(uid) + "\t" + str(rating) + "\t" + "2020-12-26" +  "\n"
        print(string)
        fd.write(string)

s3.meta.client.upload_file('/tmp/data_part2_test.txt', BUCKET_NAME, KEY)
print("done")