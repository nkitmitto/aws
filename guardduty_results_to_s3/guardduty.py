#!/usr/local/bin/python3.6
#Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/apache2.0/

#or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

import boto3
import json
import os
import datetime
import pycurl
from time import gmtime, strftime
from dateutil import parser
import MySQLdb

gd = boto3.client('guardduty')
s3 = boto3.resource('s3')

bucket = "<s3_bucket_name>"
file_path = "/tmp/"
file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + "-findings.csv"
date = strftime("%Y-%m-%d-%H:%M:%S", gmtime())

host="<HOST>"
port=<PORT>
dbname="<DBNAME>"
user="<USERNAME>"
password="<PASSWORD>"

conn = MySQLdb.connect(host, user=user,port=port,
                           passwd=password, db=dbname)

c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS attacks (
    gd_event_id VARCHAR(32) NOT NULL,
    offender_ip VARCHAR(15) NOT NULL,
    attacked_port VARCHAR(5) NOT NULL,
    last_seen DATETIME NOT NULL
    )""")

#Used to parse the JSON Serialization for time - REQUIRED
def datetime_handler(x):
    if isinstance(x, datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

 # Find the Detectors and use the first one
detectors = gd.list_detectors()
detectors_json_dumps = json.dumps(detectors)
detectors_json_loads = json.loads(detectors_json_dumps)
detector = detectors_json_loads['DetectorIds'][0]

# Grab all findings under the detector
findings = gd.list_findings(DetectorId=detector)
findings_json_dumps = json.dumps(findings)
findings_json_loads = json.loads(findings_json_dumps)

#Write headers into the file
write_headers = open(file_path + file_name,"w")
write_headers.write("ip,port")
write_headers.close()

#Check all findings assigned to the detector defined above
for i in findings_json_loads["FindingIds"]:
    get_findings = gd.get_findings(DetectorId=detector,FindingIds=[i])
    #print(get_findings)
    get_findings_json_dumps = json.dumps(get_findings, default=datetime_handler)
    get_findings_json_loads = json.loads(get_findings_json_dumps)
    if get_findings_json_loads["Findings"][0]["Service"]["Action"]["ActionType"] == "NETWORK_CONNECTION":
         if ("LocalPortDetails" or "RemoteIpDetails") not in get_findings_json_loads["Findings"][0]["Service"]["Action"]["NetworkConnectionAction"]:
             continue
         gd_event_id = get_findings_json_loads["Findings"][0]["Id"]
         offender_ip = get_findings_json_loads["Findings"][0]["Service"]["Action"]["NetworkConnectionAction"]["RemoteIpDetails"]["IpAddressV4"]
         attacked_port = str(get_findings_json_loads["Findings"][0]["Service"]["Action"]["NetworkConnectionAction"]["LocalPortDetails"]["Port"])
         last_seen =  get_findings_json_loads["Findings"][0]["Service"]["EventLastSeen"]
         last_24 = parser.parse(last_seen).strftime('%y-%m-%d %H:%M:%S')
         file = open(file_path + file_name,"a", newline='\n')
         file.write("\r\n%s,%s"  %(offender_ip, attacked_port))
         file.close()

         sql = "INSERT INTO attacks (gd_event_id,offender_ip,attacked_port,last_seen) VALUES('%s','%s','%s','%s')" % (gd_event_id, offender_ip, attacked_port, last_24)
         print(sql)

         c.execute(sql)
         conn.commit()
        

# Upload file to an S3 bucket for analysis
s3.meta.client.upload_file(file_path + file_name, bucket, file_name)
