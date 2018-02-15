#This script is meant to be used within Lambda.  This script can be setup to run on a schedule via Cloudwatch events.
#This script will delete snapshots that are older than 14 days (336 hours)
#Maintained and managed by Nick Kitmitto (nick@eccentricson.com)

import boto3
import json
from datetime import datetime
from datetime import timedelta
from dateutil import parser

client = boto3.client('ec2')

del_hours = 336
del_seconds = del_hours * 3600

#Used to parse the JSON Serialization for time - REQUIRED
def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


#Fetch Account number to filter Snapshots
account_number = boto3.client('sts').get_caller_identity()['Account']

def lambda_handler(event, context):
	#Describe the snapshots for our account
	response = client.describe_snapshots(
		Filters=[
		{
			'Name': 'owner-id',
			'Values': [account_number]
		}
		]
	)

	#Dump then load the JSON into variables
	dump_json = json.dumps(response, default=datetime_handler)
	load_json = json.loads(dump_json)

	#For loop to loop through each Snapshot in the account
	for i in load_json['Snapshots']:
		volumeid = i['VolumeId']
		starttime = i['StartTime']
		snapshotid = i['SnapshotId']
		description = i['Description']
		
		if description == '':

			#Parse the sarttime and now 
			parsed_time = parser.parse(starttime).strftime('%y-%m-%d %H:%M:%S')
			now = datetime.now().strftime('%y-%m-%d %H:%M:%S')

			#Convert the comparable formats to strings
			now_str = str(now)
			parsed_time_str = str(parsed_time)

			#Strip the strings into comparable formats
			now_stripped = datetime.strptime(now_str, "%y-%m-%d %H:%M:%S")
			parsed_time_stripped = datetime.strptime(parsed_time_str, "%y-%m-%d %H:%M:%S")

			#Calculate the difference for evaluation
			difference = parsed_time_stripped - now_stripped

			#Delete snapshot if difference.seconds is greater than the delete seconds variable at the top
			if abs(difference.total_seconds()) > del_seconds:
				client.delete_snapshot(SnapshotId=snapshotid)
			else:
				print("Not deleting snapshot %s") % snapshotid
