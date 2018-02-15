<!--- Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at

    http://aws.amazon.com/apache2.0/

or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
-->

### S3 Enforce Encryption

S3 has many easy features that can be implemented in the name of security.  Unfortunately, many people don't know that some of these features exist.  This Lambda function will encrypt new and existing S3 buckets.

**How To**

Create an IAM role with the attached policy (see below).
Place the enforce_encryption.py code into Lambda, assign it the IAM role you created. (This is Python 3.6)
Setup AWS Config with a new custom rule, set it for "Configuration Changes".
Input the ARN of the Lambda function you created and create the Config rule.
Watch your buckets become encrypted!

**IAM Policy**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "pol0",
            "Effect": "Allow",
            "Action": [
                "s3:ListAllMyBuckets",
                "s3:PutBucketPolicy",
                "s3:ListBucket",
                "s3:PutBucketEncryption",
                "s3:PutEncryptionConfiguration",
                "logs:PutLogEvents",
                "logs:CreateLogStream",
                "logs:PutDestination"
            ],
            "Resource": "*"
        }
    ]
}
```

