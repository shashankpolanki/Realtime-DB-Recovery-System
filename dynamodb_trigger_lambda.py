import json
import boto3
import os
import re
from decimal import Decimal
from datetime import datetime

print('Loading function')

"""
This function takes in a ugly nested dictionary and returns out a dictionary
"""
def clean_data(nest_dict):
    new_dict = {}
    for k,v in nest_dict.items():
        for k2,v2 in v.items():
            new_dict[k] = v2
    return new_dict


def lambda_handler(event, context):
    # Types of events to store in backup table
    must_copy = ["REMOVE", "INSERT"]

    for record in event['Records']:
        rec_type = record["eventName"]

        if rec_type in must_copy:

            block = record['dynamodb']
            time_create = block['ApproximateCreationDateTime']
            readable_time = datetime.utcfromtimestamp(time_create).strftime('%Y-%m-%d %H:%M:%S')

            # Getting the primary key of the record
            primary_key = clean_data(block['Keys'])
            # Getting the whole record
            try:
                the_image = clean_data(block['NewImage'])
            except KeyError:
                the_image = clean_data(block['OldImage'])

            """
            Figuring out which table triggered this lambda and
            where to store the backup logs
            """
            arn_address = record['eventSourceARN']
            x = re.search(r"table\/(\w+)\/", arn_address)
            name = x.group(1) + "_Backup"

            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(name)
            # try:
            response = table.put_item(
                           Item={
                                    'Time': Decimal(time_create),
                                    'Readable_Time': readable_time,
                                    'Type': rec_type,
                                    'Keys': primary_key,
                                    'Image': the_image
                                }
                        )

            print("PutItem succeeded")
            # except Exception:
            #    print("Something Went Wrong")

        print(record['eventID'])
        print(record['eventName'])
        print("DynamoDB Record: " + json.dumps(record['dynamodb'], indent=2))

    return 'Successfully processed {} records.'.format(len(event['Records']))
