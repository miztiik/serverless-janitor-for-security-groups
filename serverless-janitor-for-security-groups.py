'''
Search and delete unused AWS console launch wizard security groups
'''

import boto3
import logging
from botocore.exceptions import ClientError

# Customize the global variables as needed
globalVars  = {}
globalVars['Owner']                 = "Miztiik"
globalVars['Environment']           = "Test"
globalVars['REGION_NAME']           = "ap-southeast-2"
globalVars['findNeedle']            = "*launch-wizard*"

ec2 = boto3.client('ec2', region_name = globalVars['REGION_NAME'] )

filters = [
    {'Name': 'group-name', 'Values': [ globalVars['findNeedle'] ] }
]

def janitor_for_security_groups():
    sg_deleted = { 'SecurityGroups': [] }
    sgs = ec2.describe_security_groups(Filters=filters).get('SecurityGroups')
    for sg in sgs:
        logging.info("Attempting to delete security group: {0}, ID: {1}".format(sg.get('GroupName'), sg.get('GroupId') ))
        try:
            ec2.delete_security_group(GroupName=sg.get('GroupName'))
            sg_deleted.get('SecurityGroups').append(
                {'GroupName': sg.get('GroupName'), 'GroupId': sg.get('GroupId'), 
                'Description': sg.get('Description'), 'VpcId': sg.get('VpcId')})

        except ClientError as e:
            print(str(e.response))
            logging.error('Unable to delete Security Group with id: {0}'.format(sg.get('GroupId')) )
            logging.error('ERROR: {0}'.format( str(e.response)) )

    return sg_deleted

def lambda_handler(event, context):
    return janitor_for_security_groups()

if __name__ == '__main__':
    lambda_handler(None, None)
