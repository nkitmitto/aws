# Terraform VPC Creation

The files in here consist of the Terraform template, variables, and authentication file.  

### Requirements For Use
1. Modify aws.tf with your AWS credentials
2. Ensure you're using Terraform >0.8.8
3. Modify the variables.tf file.  Input proper CIDRs, region and VPC name
4. Understand the template - don't run anything you don't know exactly what it does

To run, execute: terraform -var-file=terraform.tfvars
