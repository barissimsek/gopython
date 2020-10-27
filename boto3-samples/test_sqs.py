import sqs
import uuid

buildID = uuid.uuid4()
print(buildID)

params = {
    'buildID': {
        'StringValue': str(buildID),
        'DataType': 'String'        
    },
    'buildName': {
        'StringValue': 'windows2019',
        'DataType': 'String'
    },
    'buildOwner': {
        'StringValue': '321',
        'DataType': 'String'
    }
}

print(sqs.send_message('buildRequests.fifo', 'build', params, str(buildID)))

buildID = uuid.uuid4()
print(buildID)

params = {
    'buildID': {
        'StringValue': str(buildID),
        'DataType': 'String'        
    },
    'buildName': {
        'StringValue': 'redhat77',
        'DataType': 'String'
    },
    'buildOwner': {
        'StringValue': '123',
        'DataType': 'String'
    }
}

print(sqs.send_message('buildRequests.fifo', 'build', params, str(buildID)))
