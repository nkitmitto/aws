# This script will take a look at the instances that are "running" in your environment and evalute the 
# launch time.  If the delta from now (When the script is run) to the launch time is greater than the
# value specified on line 13, it will terminate the instance.

# Created and maintained by Nick Kitmitto (nick@eccentricson.com)


import boto3
from dateutil import parser
import json
from datetime import datetime
from datetime import timedelta
client = boto3.client('ec2')

term_hours = 2
term_seconds = term_hours * 3600

# Handle Datetime for Expiration in the AWS API call
def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

response = client.describe_instances(
	Filters=[
	   {
		'Name': 'tag:Docker-Created',
		'Values': ['True']
	   },
	   {
	    'Name': 'instance-state-name',
	    'Values': ['running']
	   }
	]
)

dump = json.dumps(response, default=datetime_handler)
load = json.loads(dump)
reservations = load['Reservations'][0]
launchtime = reservations['Instances'][0]['LaunchTime']
instance_id = reservations['Instances'][0]['InstanceId']
parsed_time = parser.parse(launchtime).strftime('%m-%d %H:%M:%S')

now = datetime.now().strftime('%m-%d %H:%M:%S')
now_str = str(now)
parsed_time_str = str(parsed_time)

now_stripped = datetime.strptime(now_str, "%m-%d %H:%M:%S")
parsed_time_stripped = datetime.strptime(parsed_time_str, "%m-%d %H:%M:%S")

difference = parsed_time_stripped - now_stripped

if difference.seconds > term_seconds:
	client.terminate_instances(InstanceIds=[instance_id])
else:
	print "Not terminating instance"
