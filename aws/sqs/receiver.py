import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='Photo-stream.fifo')

print queue

# Process messages by printing out body
for message in queue.receive_messages():
	print(message.body)
	# you should process the message here

	# Delete the message after it is processed 
	message.delete()





