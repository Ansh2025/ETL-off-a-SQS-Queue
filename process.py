# Importing Libraries
import json
import boto3
import base64
import config
import psycopg2

from datetime import datetime

def connect(endpoint_url):
    """
    Creating a client to receive messages from the LocalStack Docker 

    Args:
        endpoint_url (string): url to receive the AWS SQS records

    Returns:
        object: Returns the client object
    """

    client = boto3.client('sqs',endpoint_url= endpoint_url)
    return client



def get_message(client,endpoint_url, queue_name):
    """
    This method returns the message in the JSON format which was received by the client
    The number of messages and the waitTimeSeconds can be adjusted according the user's requirement

    Args:
        client (object): boto3 client object
        endpoint_url (string): url to receive the AWS SQS records
        queue_name (string): name if the SQS queue

    Returns:
        reponse: This method returns the JSON response
    """
    response = client.receive_message(
        QueueUrl= endpoint_url + "/" +  queue_name,
        MaxNumberOfMessages=config.MaxNumberOfMessages,
        WaitTimeSeconds=config.WaitTimeSeconds,
    )
    return response


def encode_message(original_text):
    """"
    This method is to used to encode the 'ip' and 'device_id' in base64
    First we enconde the message in ascii format then we encode it into base64

    Args:
        original_text (string): String that is needed to be encrypted

    Returns:
        string: Returns the encrypted string
    """
    ascii_string = original_text.encode('ascii')
    encoded_string = base64.b64encode(ascii_string).decode('utf-8')
    return encoded_string


def create_formatted_message(responses):
    """
    The create_formatted_message methos is used to extract relevant information from the JSON response
    and create a formatted message to write into postgres database

    Args:
        responses (JSON): Response message received from client

    Returns:
        list: Formatted message that is neccessary to insert data into postgres database
    """
    messages  = responses['Messages']
    message_list = []
    for message in messages:
        body = json.loads(message['Body'])
        user_id =body['user_id']
        device_type = body['device_type']
        masked_ip = encode_message(body['ip'])
        masked_device_id = encode_message(body['device_id'])
        locale = body['locale']
        app_version = body['app_version']
        create_date = datetime.now().strftime("%Y-%m-%d")

        message_tuple = (user_id,device_type,masked_ip,masked_device_id,locale,app_version,create_date)
        message_list.append(message_tuple)

    return message_list

def insert_into_psql(user_list):
    """
    This method is used to connect the process python file with the postgre database and 
    write the data into the database

    Args:
        user_list (list): formatted message that is used to send the data into the postgres database
    """

    sql = "INSERT INTO user_logins(user_id,device_type,masked_ip,masked_device_id,locale,app_version,create_date) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    conn = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=config.dbname, user=config.user, password=config.password)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,user_list)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    """
    This is the main method from where this python cript starts.
    This methods calls the neccessary functions in their respective order
    """

    client = connect(config.endpoint_url)
    responses = get_message(client,config.endpoint_url,config.queue_name)
    message_list = create_formatted_message(responses)
    insert_into_psql(message_list)
