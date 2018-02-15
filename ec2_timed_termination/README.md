# Evaluate launch time for EC2 instances

 This script will take a look at the instances that are "running" in your environment and evalute the 
 launch time.  If the delta from now (When the script is run) to the launch time is greater than the
 value specified on line 13, it will terminate the instance.

##Maintainer
Nick Kitmitto (nick@eccentricson.com)

##Requirements
Python
AWS cli access with credentials in ~/.aws/credentials
