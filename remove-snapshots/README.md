# Remove snapshots older than 14 days

This tool will remove snapshots older than 14 days

## Maintainer
Nick Kitmitto (nick@eccentricson.com)

## Requirements
Lambda function created with the python script and utilizing the IAM role below.
CloudWatch Events schedule to kick the job off

## IAM Role Capability Requirements

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1479495079000",
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeSnapshots",
                "ec2:DeleteSnapshot"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}
```
