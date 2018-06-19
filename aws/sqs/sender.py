import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='Photo-stream.fifo')

print queue

data = "{ \
	'path': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png', \
	'width': 800, \
	'height': 600 \
}"

# send message to the AWS queue
response = queue.send_message(
    MessageBody=data,
    MessageGroupId='messageGroup1',
    MessageDeduplicationId='unique-key-word'  # This normally should be hash of the body
)

print response


