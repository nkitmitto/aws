# Remove Restricted Ingress Ports

 The python script included in this repo will remove restricted ports from security group ingress rules that are open to the internet.


**For example:**

	Security Group has 22 open to 0.0.0.0/0 - this ingress rule would be removed

	Security Group has 22 open to 192.168.0.0/16 - this ingress rule would remain

## Maintainer
Nick Kitmitto (nick@eccentricson.com)

## Requirements
AWS Configured and pointed to an SNS topic

Lambda configured with the SNS topic trigger

## IAM Role Capability Requirements

Assign the following policy to your Lambda role to allow this script to function:

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1479339143675",
      "Action": [
        "ec2:DeleteSecurityGroup",
        "ec2:DescribeSecurityGroups",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```
 
## Troubleshooting
The logs of this Lambda script will be recorded to CloudWatch Logs.  If you have issues, check the CloudWatch logs for more information
