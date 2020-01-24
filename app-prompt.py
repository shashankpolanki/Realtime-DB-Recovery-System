"""
Objective: Script that prompts the user with options on what
table to recover and from what time period.

"""
import boto3


def get_prod_tables():
    dynamodb_client = boto3.client('dynamodb')
    # Get all tables and remove the ones with _Backup in them
    all_tables = dynamodb_client.list_tables()['TableNames']
    # Get production tables not backup tables
    prod_tables = list()
    for x in all_tables:
        if len(x) <= 7 or x[len(x) - 7:] != "_Backup":
            prod_tables.append(x)
    return prod_tables


def get_table_obj(table_name):
    # If a backup table is wanted then pass in table_name + _underscore
    dynamodb = boto3.resource('dynamodb')
    selected_table = dynamodb.Table(table_name)
    return selected_table


def get_table_items(selected_table):
    response = (selected_table.scan())['Items']
    return response


def insert_item(selected_table, data_blob):
    # In the case an error happens it needs to be logged in cloudwatch/logfile
    response = selected_table.put_item(
       Item=data_blob
    )
    return response


def delete_item(selected_table, key):
    response = selected_table.delete_item(
        Key=key
    )
    return response


if __name__ == "__main__":
    """
    Prompt the user about what records to recover and recover them...
    """
    print("Which table would you like to recover?")
    print(get_prod_tables())
    choice = input("Enter here --> ")

    recovery_table = get_table_obj(choice + "_backup")

    recov_table_items = get_table_items(recovery_table)
    for x, y in enumerate(recov_table_items):
        print(x, y['Readable_Time'], y['Type'])

    left_choice = input("Select Recovery Start Point ==> ")
    right_choice = input("Select Recovery End Point ==> ")

    prod_table = get_table_obj(choice)
    for idx in range(right_choice, left_choice-1, -1):
        type = recov_table_items[idx]['Type']
        key = recov_table_items[idx]['Keys']
        image = recov_table_items[idx]['Image']
        # Do the opposite of what is there.
        if type == "INSERT":
            # Call delete function that takes in the table name, key
            delete_item(prod_table, key)
        elif type == "DELETE":
            # Call delete function that takes in the table name and image
            insert_item(prod_table, image)

    print("Recovery is complete")
