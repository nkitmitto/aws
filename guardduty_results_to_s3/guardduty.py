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
#import MySQLdb

gd = boto3.client('guardduty')
s3 = boto3.resource('s3')
ec2 = boto3.client('ec2')

bucket = "nk-gd-findings"
file_path = "/tmp/"
file_name = strftime("%Y-%m-%d-%H:%M:%S", gmtime()) + "-findings.csv"
date = strftime("%Y-%m-%d-%H:%M:%S", gmtime())
network_connection_violation = 1
port_probe_violation = 1

host="<HOST>"
port="<PORT>"
dbname="<DBNAME>"
user="<USERNAME>"
password="<PASSWORD>"

#conn = MySQLdb.connect(host, user=user,port=port,
#                           passwd=password, db=dbname)

#c = conn.cursor()
#c.execute("""CREATE TABLE IF NOT EXISTS attacks (
#    gd_event_id VARCHAR(32) NOT NULL,
#    offender_ip VARCHAR(15) NOT NULL,
#    attacked_port VARCHAR(5) NOT NULL,
#    last_seen DATETIME NOT NULL
#    )""")

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
findings = gd.list_findings(DetectorId=detector, FindingCriteria={'Criterion':{'service.archived':{'Neq':['True']}}})
findings_json_dumps = json.dumps(findings)
findings_json_loads = json.loads(findings_json_dumps)

#Write headers into the file
write_headers = open(file_path + file_name,"w")
write_headers.write("ip,port")
write_headers.close()

current_rule_numbers = []
current_ips = []
#VPC NACL Rule Numbers
def nacl_rule_numbers():
    for n in desc_nacls['NetworkAcls']:
        for e in n['Entries']:
            if 99 < e['RuleNumber'] < 32766:
                current_rule_numbers.append(e["RuleNumber"])
                
    new_rule = current_rule_numbers[-1]
    return(new_rule)
#VPC NACL Blocked IPs
def nacl_ips():
    for n in desc_nacls['NetworkAcls']:
        for e in n['Entries']:
            current_ips.append(e['CidrBlock'])

    all_nacl_ips = current_ips
    return(all_nacl_ips)

def desc_instances():
    try:
        global desc_instance
        desc_instance = ec2.describe_instances(InstanceIds=[instance_id])
        return(desc_instance)
    except:
        print("Terrible error occurred")


#Check all findings assigned to the detector defined above
for i in findings_json_loads["FindingIds"]:
    get_findings = gd.get_findings(DetectorId=detector,FindingIds=[i])
    get_findings_json_dumps = json.dumps(get_findings, default=datetime_handler)
    get_findings_json_loads = json.loads(get_findings_json_dumps)
    if get_findings_json_loads["Findings"][0]["Service"]["Action"]["ActionType"] == "PORT_PROBE":
#         if ("LocalPortDetails" or "RemoteIpDetails") not in get_findings_json_loads["Findings"][0]["Service"]["Action"]["PortProbeAction"]["PortProbeDetails"]:
#            print("Local Port Details = " + str(get_findings_json_loads["Findings"][0]["Service"]["Action"]["PortProbeAction"]["PortProbeDetails"][0]["LocalPortDetails"]["Port"]))
#            print("Remote IP Details = " + get_findings_json_loads["Findings"][0]["Service"]["Action"]["PortProbeAction"]["PortProbeDetails"][0]["RemoteIpDetails"]["IpAddressV4"])
#            continue
         gd_event_id = get_findings_json_loads["Findings"][0]["Id"]
         offender_ip = get_findings_json_loads["Findings"][0]["Service"]["Action"]["PortProbeAction"]["PortProbeDetails"][0]["RemoteIpDetails"]["IpAddressV4"] + "/32"
         attacked_port = str(get_findings_json_loads["Findings"][0]["Service"]["Action"]["PortProbeAction"]["PortProbeDetails"][0]["LocalPortDetails"]["Port"])
         last_seen =  get_findings_json_loads["Findings"][0]["Service"]["EventLastSeen"]
         last_24 = parser.parse(last_seen).strftime('%y-%m-%d %H:%M:%S')
         count = get_findings_json_loads["Findings"][0]["Service"]["Count"]
         file = open(file_path + file_name,"a", newline='\n')
         file.write("\r\n%s,%s,%s"  %(offender_ip, count, attacked_port))
         file.close()
         if count >= network_connection_violation:
          if get_findings_json_loads["Findings"][0]["Resource"]["ResourceType"] == "Instance":
            instance_id = get_findings_json_loads["Findings"][0]["Resource"]["InstanceDetails"]["InstanceId"]
            print(instance_id)
            desc_instances()
            vpc = desc_instance["Reservations"][0]["Instances"][0]["VpcId"]
            desc_nacls = ec2.describe_network_acls(Filters=[{'Name':'vpc-id', 'Values': [vpc]}])
            nacl_id = desc_nacls["NetworkAcls"][0]["NetworkAclId"]
            nacl_rule_numbers()
            nacl_ips()
            if offender_ip in current_ips:
              print("%s is already blocked in the NACL %s" % (offender_ip, nacl_id))
            else:
              ec2.create_network_acl_entry(CidrBlock=(offender_ip), Egress=False, NetworkAclId=nacl_id, Protocol="-1", RuleAction='deny', RuleNumber=current_rule_numbers[-1] + 1)
              print("Blocked IP %s for attacking %s on port %s" %(offender_ip, instance_id, attacked_port))

#         sql = "INSERT INTO attacks (gd_event_id,offender_ip,attacked_port,last_seen) VALUES('%s','%s','%s','%s')" % (gd_event_id, offender_ip, attacked_port, last_24)
#         print(sql)

#         c.execute(sql)
#         conn.commit()
        

# Upload file to an S3 bucket for analysis
#s3.meta.client.upload_file(file_path + file_name, bucket, file_name)
