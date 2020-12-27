import boto3
import botocore
import json
import random
import time
import logging
import random
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
# --------------------------- set dynamodb for get info   ------------------------
dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('user_info')
 
# --------------------------- store phone number for lf3   ------------------------
def store_info(phone, name):
    # print(type(expiration_time))
    user_table.put_item(
        Item={
            "uid":"6000",
            "phone":phone,
            "name" : name,
        }
    )
# --------------------------- get INFO from event   ------------------------
def get_info(event):
    body = event
    if "messages" not in body:
        return None,None,None
    messages = event["messages"]
    if not isinstance(messages,list) or len(messages) < 1:
        logger.error("no message")
        return None,None,None
    message = messages[0]
    if "unconstructed" not in message:
        logger.error("message missing unconstructed")
        return None,None,None
    name = message["unconstructed"]["name"]
    phone = message["unconstructed"]["phone"]
    rating = message["unconstructed"]["rating"]
    
    return name, phone, rating
    
def lambda_handler(event, context):
    print("event is:",event)
    name,phone,rating = get_info(event)
    print("name is:", name)
    print("phone is:", phone)
    print("rating is:", rating)
    rating_int = int(rating)
    rating_arr = []
    while rating_int > 0:
        curr_rating = rating_int % 10
        rating_arr.append(curr_rating)
        rating_int = rating_int / 10
    res_arr = rating_arr[::-1]
    print("res_arr is :" + str(res_arr))
    movie_id = [1,24,12,10,18]
# ----------- Save rating info to s3 ----------------------------------------
    BUCKET_NAME = 'cc-final-proj' 
    KEY = 'data_part2_test.txt'
    LOCAL_FILE = '/tmp/data_part2_test.txt'
    s3 = boto3.resource('s3')
    try:
        #s3.Bucket('mybucket').download_file('hello.txt', '/tmp/hello.txt')
        obj=s3.Bucket(BUCKET_NAME).download_file(KEY,LOCAL_FILE)
        print("Found obj file")
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
        else:
            print("Other errors")
    with open('/tmp/data_part2_test.txt', 'a') as fd:
        uid = 6000
        print("open file ok")
        for i in range(len(res_arr)):
            print("----- i  " + str(i))
            mid = movie_id[i] # movie in range in the rating dataset
            rating = res_arr[i] # rating data from user input
            string = str(mid) + "\t" + str(uid) + "\t" + str(rating) + "\t" + "2020-12-27" +  "\n"
            print(string)
            fd.write(string)
    new_key = "data_part2_test_new.txt"
    # s3.meta.client.upload_file('/tmp/hello.txt', 'mybucket', 'hello.txt')
    s3.meta.client.upload_file('/tmp/data_part2_test.txt', BUCKET_NAME, new_key)
    store_info(phone,name)
    print("done")
    #----------- Uncomment ----------------------#
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
