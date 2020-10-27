__author__ = 'Baris Simsek'

import boto3

userData = '''#!/bin/bash
yum update -y
echo "Hello World" > /root/welcome.txt
'''

def create_instance(buildID):
    ec2 = boto3.resource('ec2', region_name="us-east-1")

    instances = ec2.create_instances(
	    ImageId='ami-0affd4508a5d2481b', 
	    MinCount=1, 
	    MaxCount=1,
	    KeyName="mykey",
	    InstanceType="t2.micro",
        SubnetId='subnet-09603t37',
        SecurityGroupIds= [
            "sg-1f653708"
        ],
        UserData=userData
    )

    tags = [{'Key': 'Name', 'Value': buildID}]

    instanceID = instances[0].id

    create_ec2_tags([instanceID], tags)

    return instanceID

def create_ec2_tags(instanceList, tags):
    ec2 = boto3.resource('ec2', region_name="us-east-1")

    ec2.create_tags(Resources=instanceList, Tags=tags)

def stop_ec2_instance(instanceList):
    print('Stopping instance: ', instanceList)
    ec2 = boto3.resource('ec2', region_name="us-east-1")

    ec2.instances.filter(InstanceIds = instanceList).stop()

    return 0

def terminate_ec2_instance(instanceList):
    ec2 = boto3.resource('ec2', region_name="us-east-1")

    ec2.instances.filter(InstanceIds = instanceList).terminate()

    return 0

def create_image(instanceID, instanceName):
    ec2 = boto3.resource('ec2', region_name="us-east-1")

    ec2.create_image(InstanceId=instanceID, Name="abc")

    return 0
