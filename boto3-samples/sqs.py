'''
Author: Baris Simsek
'''

import boto3
import uuid

def send_message(queueName, message, params, mdid):
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=queueName)

    # Create a new message
    response = queue.send_message(
        MessageBody=message,
        DelaySeconds=0,
        MessageGroupId='messageGroup1',
        MessageDeduplicationId=mdid,
        MessageAttributes=params
    )

    return response

def receive_messages(queueName):
    buildJobs = []

    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=queueName)

    # Process messages by printing out body
    for message in queue.receive_messages(MessageAttributeNames=['buildID', 'buildName', 'buildOwner']):
        buildID = message.message_attributes.get('buildID').get('StringValue')
        buildName = message.message_attributes.get('buildName').get('StringValue')
        buildOwner = message.message_attributes.get('buildOwner').get('StringValue')

        buildJobs.append({'buildID': buildID, 'name': buildName, 'owner': buildOwner})

        # Delete the message
        message.delete()

    return buildJobs
