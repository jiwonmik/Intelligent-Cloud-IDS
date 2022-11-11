import collections
from collections import defaultdict
import boto3
import time
from datetime import datetime

session = boto3.Session()
# Connect to EC2 & DynamoDB
ec2 = session.client('ec2')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Spec')

ec2info = defaultdict()
instance_list = ec2.describe_instances(Filters=[{
    'Name': 'instance-state-name',
    'Values': ['running']}])

for reservation in instance_list["Reservations"]:
    for instance in reservation.get("Instances", []):
        for tag in instance["Tags"]:
            if 'Name' in tag['Key']:
                name = tag['Value']
        launch_time = instance["LaunchTime"]
        launch_time_friendly = launch_time.strftime("%B %d %Y")
        NetworkInterfaces = instance.get("NetworkInterfaces")
        BlockDeviceMappings = instance.get("BlockDeviceMappings")
        mac_address = NetworkInterfaces[0]['MacAddress']
        network_interface_id= NetworkInterfaces[0]['NetworkInterfaceId']
        network_interface_owner_id = NetworkInterfaces[0]['OwnerId']

        ec2info = {
            "Instance ID": instance["InstanceId"],
            "Image Id": instance["ImageId"],  
            "Instance Name": name,  
            "Instance Type": instance["InstanceType"],
            "State": instance["State"]["Name"],
            "Private IP": instance["PrivateIpAddress"],
            "Public IP": instance["PublicIpAddress"],
            "MAC Address": mac_address,
            "Private DNS Name": instance['PrivateDnsName'],
            "Public DNS Name": instance['PublicDnsName'],
            "Subnet ID": instance['SubnetId'],
            "VPC ID": instance['VpcId'],
            "IAM Instance ARN": instance["IamInstanceProfile"]["Arn"],
            "IAM Instance ID": instance["IamInstanceProfile"]["Id"],
            "NetworkInterface ID": network_interface_id,
            "NetworkInterface Owner ID": network_interface_owner_id,
            "CPU Options": {
                'Core Count': instance["CpuOptions"]["CoreCount"],
                'Threads Per Core': instance["CpuOptions"]["ThreadsPerCore"]
            },
            "Availability Zone": instance["Placement"]["AvailabilityZone"],
            "Launch Time": launch_time_friendly,
            "Architecture": instance["Architecture"]
        }

        attributes = ['Instance ID', 'Image Id', 'Instance Type', 'Instance Name',
        'State', 'Private IP', 'Public IP', 'MAC Address', 'Private DNS Name', 'Public DNS Name', 'Subnet ID', 'VPC ID', 'IAM instance ARN', 'IAM Instance ID', 'NetworkInterface ID', 'NetworkInterface Owner ID',
                      'CPU Options', 'Availability Zone', 'Launch Time', 'Architecture']

        for instance in ec2info.items():
            print(instance)
            print("------")
        table.put_item(Item=ec2info)
