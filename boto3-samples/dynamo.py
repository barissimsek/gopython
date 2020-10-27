__author__ = 'Baris Simsek'

import boto3
from botocore.exceptions import ClientError

def update_build_status(tableName, buildID, buildStatus):
    ddb = boto3.resource('dynamodb')
    table = ddb.Table(tableName)

    try:
        response = table.update_item(
            Key={
                'build_id': buildID
            },
            UpdateExpression = "set build_status = :buildStatus",
            ExpressionAttributeValues = {
                ":buildStatus": buildStatus
            },
            ReturnValues="UPDATED_NEW"
        )
    except ClientError as e:
        print("Client error: ", e)
    else:
        print(response)
        return response

    print("here")

    return response
    