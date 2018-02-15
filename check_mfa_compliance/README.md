# Require MFA

This tool will notify an SNS topic when an IAM user does not have an MFA token setup on their account.

##Maintainer
Nick Kitmitto (nick@eccentricson.com)

##Requirements
AWS Config created with an SNS Topic
Lambda function created with the python script and utilizing the IAM role below.

##IAM Role Capability Requirements

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1479495079000",
            "Effect": "Allow",
            "Action": [
                "iam:GetLoginProfile",
                "iam:GetUser",
                "iam:ListAccessKeys",
                "iam:ListUsers",
                "iam:ListVirtualMFADevices",
                "iam:ListMFADevices",
                "config:PutEvaluations",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
