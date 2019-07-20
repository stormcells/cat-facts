import json
import boto3
import random
import os

def lambda_handler(event, context):
    bucket = 'obligations'
    key = 'catfacts.json'
    
    try:
        s3 = boto3.resource('s3')
        data = s3.Object(bucket, key)
        print("Got the data: ", data)
        
        parsed_json = json.loads(data.get()['Body'].read().decode('utf-8)'));
        fact = random.choice(parsed_json['facts'])
        print('fact = {}'.format(fact))
        
        if os.environ['SNS_ENABLED'] == 'TRUE':
            client = boto3.client('sns')
            response = client.publish(
                TargetArn=os.environ['TOPIC_ARN'],
                Message=json.dumps({'default': json.dumps(fact)}),
                MessageStructure='json'
            )
            print('Sns sent...')
        return fact;
    except Exception as e:
        print(e)
        raise e
