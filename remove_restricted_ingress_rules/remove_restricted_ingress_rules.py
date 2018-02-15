from __future__ import print_function
import json
import boto3

print('Loading function')
ec2 = boto3.client('ec2')
restricted_ports = ['22','3389','3306','1433']


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    msg = json.loads(event['invokingEvent'])
    result_token = event["resultToken"]
    
    for rp in restricted_ports:
        for permissions in msg['configurationItem']['configuration']['ipPermissions']:
            for ip in permissions['ipRanges']:
                configuration = msg['configurationItem']['configuration']
                sgname = configuration['groupName']
                sgid = configuration['groupId']
                strsgid = str(sgid)
                fromport = int(permissions['fromPort'])
                toport = int(permissions['toPort'])
                ipprotocol = str(permissions['ipProtocol'])
                prefixlistids_array = permissions['prefixListIds']
                if ip == "0.0.0.0/0"and ipprotocol != "-1" and sgname != "Jumphost" and (int(toport) == int(rp) or int(fromport) == int(rp)):
                    status = "NON_COMPLIANT"
                    config = boto3.client("config")
                    response = config.put_evaluations(
                        Evaluations=[
                            {
                                "ComplianceResourceType":
                                    'AWS::EC2::SecurityGroup',
                                "ComplianceResourceId":
                                    sgid,
                                "ComplianceType":
                                    status,
                                "Annotation":
                                    'Has restricted ports open',
                                "OrderingTimestamp":
                                    msg['configurationItem']['configurationItemCaptureTime']
                            },
                        ],
                        ResultToken=result_token
                    )
                    response = ec2.revoke_security_group_ingress(
                        DryRun = False,
                        IpProtocol = ipprotocol,
                        FromPort = fromport,
                        ToPort = toport,
                        CidrIp =  ip,
                        GroupId = strsgid
                    )

                elif "launch-wizard" in sgname:
                    status = "NON_COMPLIANT"
                    config = boto3.client("config")
                    response = config.put_evaluations(
                        Evaluations=[
                            {
                                "ComplianceResourceType":
                                    'AWS::EC2::SecurityGroup',
                                "ComplianceResourceId":
                                    sgid,
                                "ComplianceType":
                                    status,
                                "Annotation":
                                    'Has restricted ports open',
                                "OrderingTimestamp":
                                    msg['configurationItem']['configurationItemCaptureTime']
                            },
                        ],
                        ResultToken=result_token
                    )
                    delete_response = ec2.delete_security_group(
                        DryRun=False,
                        GroupId=strsgid
                    )
                    delete_response
                else:
                    status = "COMPLIANT"
                    config = boto3.client("config")
                    response = config.put_evaluations(
                        Evaluations=[
                            {
                                "ComplianceResourceType":
                                    'AWS::EC2::SecurityGroup',
                                "ComplianceResourceId":
                                    sgid,
                                "ComplianceType":
                                    status,
                                "Annotation":
                                    'Does not have restricted ports open.',
                                "OrderingTimestamp":
                                    msg['configurationItem']['configurationItemCaptureTime']
                            },
                        ],
                        ResultToken=result_token
                    )
