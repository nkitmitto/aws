<!--- Copyright [first edit year]-[latest edit year] Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
-->

### GuardDuty Offender IPs and Attacked Ports to S3

This Lambda function will allow the end-user to get the findings from GuardDuty, place them into S3 in a CSV format.  Therefore, enabling the user to build tables, charts, pie graphs, anything to help them analyze the data as far as attacked port and attacker IP.

**How To**

Create an IAM role with the attached policy (see below). (Modify the bucket name in the IAM policy)
Create an S3 bucket.
Modify the guardduty.py script and change bucket to your own bucket.
Take the guardduty.py script, place it into a new Lambda Python 3.6 function.
Configure the Lambda function to utilize the IAM role you created.

**IAM Policy**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Pol1",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:AbortMultipartUpload",
                "guardduty:GetThreatIntelSet",
                "s3:DeleteObjectVersion",
                "guardduty:GetIPSet",
                "s3:DeleteObject",
                "s3:PutBucketVersioning"
            ],
            "Resource": [
                "arn:aws:guardduty:*:*:detector/*/ipset/*",
                "arn:aws:guardduty:*:*:detector/*/threatintelset/*",
                "arn:aws:s3:::nk-gd-findings"
            ]
        },
        {
            "Sid": "Pol2",
            "Effect": "Allow",
            "Action": [
                "guardduty:ListIPSets",
                "guardduty:GetFindings",
                "guardduty:ListThreatIntelSets",
                "guardduty:GetThreatIntelSet",
                "guardduty:GetMasterAccount",
                "guardduty:GetIPSet",
                "guardduty:ListFindings",
                "guardduty:GetMembers",
                "guardduty:GetFindingsStatistics",
                "guardduty:GetDetector",
                "guardduty:ListMembers"
            ],
            "Resource": "arn:aws:guardduty:*:*:detector/*"
        },
        {
            "Sid": "Pol3",
            "Effect": "Allow",
            "Action": [
                "guardduty:ListDetectors",
                "guardduty:GetInvitationsCount",
                "guardduty:ListInvitations"
            ],
            "Resource": "*"
        }
    ]
}
```
**Cool Things to Do**

Now create a new QuickSight analysis, use the Manifest file in this code.  Don't forget to change the bucket as well.
Visualize in a table, and you'll be able to easily read what IP is attacking what port in your networking, along with how many times.
You could even pipe it into Splunk as well, and run additional cool analytics against the data.
