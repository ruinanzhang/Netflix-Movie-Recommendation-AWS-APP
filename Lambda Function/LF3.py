import json
import boto3
import botocore
import json
import time
import logging
# from boto3.dynamodb.conditions import Key, Attr
# from botocore.exceptions import ClientError
from StringIO import StringIO # Python 2.x
# import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# ------------------------ from s3 get spark result  ------------------------ 
movie_ids = []
def get_rec_res():
	s3 = boto3.resource('s3')
	bucket = s3.Bucket('cc-final-result')
	for obj in bucket.objects.filter(Prefix = 'result_folder/part'):
		body = obj.get()['Body'].read()
		content = body.split("\n")[1:11] # drop header
		# df = pd.read_csv(StringIO(csv_string))
		for row in content:
			print("---- row :" + str(row))
			data_list = row.split(',')
			if int(data_list[1]) <= 26:
				movie_ids.append(data_list[1])
	print("---- movie_ids :" + str(movie_ids))
	logger.debug('movie_ids : {}'.format(movie_ids))
	return movie_ids


# ------------------------  from db get movie title ------------------------ 
dynamodb = boto3.resource('dynamodb')
movie_titles = dynamodb.Table('movie_titles')
recommendations = []

def get_movie_info(movie_ids):
	for id in movie_ids:
		print(" ----- id " + id)
		logger.debug('id in movie_ids : {}'.format(id))
		item = movie_titles.get_item(Key = {"movieId": str(id)})
 		print("------ movie item :" + str(item))
		recommendations.append(item['Item']['title'])
		logger.debug('movie_item : {}'.format(item))
		logger.debug('recommendations : {}'.format(recommendations))
	return recommendations	



# ------------------------  send sns ------------------------ 
     # format msg
def format_msg(recommendations):
	 # get user info
	user_info = dynamodb.Table('user_info')	 
	item = user_info.get_item(Key = {'uid': "6000"})
	username = item['Item']['name']
	# username = 'stacey'
	phone = item['Item']['phone']
	msg_part1 = "Hello " + username +  "! \nThank you for your waiting!\n" + "Here is your personalized Netflix Movie Recommendations : \n"
	msg_part2 = ""
	for rec in recommendations[:6]:
		msg_part2  = msg_part2 + "\n" + rec
	text_message = msg_part1 + msg_part2	
	print(text_message)
	return text_message,phone


def send_sns(text_message,phone):
    sns = boto3.client('sns',region_name='us-west-2')
    # for Email
    response = sns.publish(
        TopicArn='arn:aws:sns:us-west-2:964570262610:sendMovieRecommendation',
        Message= text_message,   
        Subject='Recommendation Movies',
        )
    # for Phone
    # phone ='9496685999'
    phone = "+1 "+ phone.strip()
    logger.info("------ phone in sns: " + phone)
    print("------ phone in sns: " + phone)
    response_2 = sns.publish(
     	PhoneNumber= phone,
     	Message = text_message,
    )
    

# ------------------------  main function ------------------------ 
def lambda_handler(event, context):
    # TODO implement
    movie_ids = get_rec_res()
    recommendations = get_movie_info(movie_ids)
    text, phone = format_msg(recommendations)
    send_sns(text, phone)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
