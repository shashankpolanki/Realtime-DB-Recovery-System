# In our case, the table has a unique id, name, and age
# Docker Run passes in env variables
# sudo docker run -e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY gen_data2


import random
import boto3
import os

dynamodb = boto3.resource(service_name = 'dynamodb',
                          region_name = 'us-east-2',
                          aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID'],
                          aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'])

table = dynamodb.Table('Dummy')

for x in range(5):
    # Generate a random id
    id_num = random.randint(0, 100000)
    id = str(id_num)

    # Generate a random name
    str_length = random.randint(1, 20)
    str_arr = []
    for x in range(str_length):
        char_num = random.randint(97, 122)
        the_char = chr(char_num)
        str_arr.append(the_char)
    name = "".join(str_arr)

    # Generate a random age
    age = random.randint(1, 121)

    # Add to table
    response = table.put_item(
        Item={
              'User_Id': id,
              'Name': name,
              'Age': age
        }
    )

print("Randomly Generated Records Have Been Added")
