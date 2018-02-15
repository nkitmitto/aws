import json
import boto3

APPLICABLE_RESOURCES = ["AWS::IAM::User"]

def evaluate_compliance(configuration_item):
    if configuration_item["resourceType"] not in APPLICABLE_RESOURCES:
        return "NOT_APPLICABLE"

    global user_name
    user_name = configuration_item["configuration"]["userName"]

    iam = boto3.client("iam")
    mfa = iam.list_mfa_devices(UserName=user_name)

    if len(mfa["MFADevices"]) > 0:
        return "COMPLIANT"
    else:
        return "NON_COMPLIANT"

def lambda_handler(event, context):
    invoking_event = json.loads(event["invokingEvent"])
    print json.dumps(event)
    configuration_item = invoking_event["configurationItem"]
    result_token = "No token found."
    if "resultToken" in event:
        result_token = event["resultToken"]


    config = boto3.client("config")
    config.put_evaluations(
        Evaluations=[
            {
                "ComplianceResourceType":
                    configuration_item["resourceType"],
                "ComplianceResourceId":
                    configuration_item["resourceId"],
                "ComplianceType":
                    evaluate_compliance(configuration_item),
                "Annotation":
                    evaluate_compliance(configuration_item),
                "OrderingTimestamp":
                    configuration_item["configurationItemCaptureTime"]
            },
        ],
        ResultToken=result_token
    )
    
    snsclient = boto3.client('sns')
    
    if evaluate_compliance(configuration_item) == "NON_COMPLIANT":
        response = snsclient.publish(
            TopicArn='arn:aws:sns:us-west-2:730621689362:lambda_alerts',
            Message="%s does not have an MFA set" % user_name,
            Subject='Noncompliant User and MFA',
            MessageStructure='Complaint'
        )
