
# AWS Serverless Janitor for launch-wizard Security Groups
This AWS Lambda function searches for all AWS Console created "launch-wizard" security groups and attempts to delete them. It returns a `json` object of all security groups successfully deleted by the function.

# Customizations
The script is designed to run only in one region, that can be customized to suit your region using the `globalVars['REGION_NAME']`. It also looks for the string `*launch-wizard*` to identify the SG's to be deleted. Change this to suit your needs

#### Output
```json
{
  "SecurityGroups": [
    {
      "GroupName": "launch-wizard-2",
      "VpcId": "vpc-6ca51a08",
      "GroupId": "sg-2a0b3a53",
      "Description": "launch-wizard-2 created 2018-05-23T23:09:40.338+02:00"
    },
    {
      "GroupName": "launch-wizard-1",
      "VpcId": "vpc-6ca51a08",
      "GroupId": "sg-cb0b3ab2",
      "Description": "launch-wizard-1 created 2018-05-23T23:09:11.975+02:00"
    },
    {
      "GroupName": "launch-wizard-3",
      "VpcId": "vpc-6ca51a08",
      "GroupId": "sg-f602338f",
      "Description": "launch-wizard-3 created 2018-05-23T23:09:53.464+02:00"
    }
  ]
}
```
#### Errors
If there is any difficulty in deleting the SG, the messages are logged. If you are running it as a lambda function, cloudwatch logs should have them. The typical error logs looks like below, for example, when there is a dependency on the security group
```json
{
  "ResponseMetadata": {
    "RetryAttempts": 0,
    "HTTPStatusCode": 400,
    "RequestId": "0873413d-ec2e-4947-917f-1e9bb8592683",
    "HTTPHeaders": {
      "transfer-encoding": "chunked",
      "date": "Wed, 23 May 2018 21:12:56 GMT",
      "connection": "close",
      "server": "AmazonEC2"
    }
  },
  "Error": {
    "Message": "resource sg-56532d2f has a dependent object",
    "Code": "DependencyViolation"
  }
}
[ERROR]	2018-05-23T21:12:56.606Z	0f64fa84-5ece-11e8-aa04-1dec995f0239	Unable to delete Security Group with id: sg-56532d2f
[ERROR]	2018-05-23T21:12:56.626Z	0f64fa84-5ece-11e8-aa04-1dec995f0239	ERROR: {
  "ResponseMetadata": {
    "RetryAttempts": 0,
    "HTTPStatusCode": 400,
    "RequestId": "0873413d-ec2e-4947-917f-1e9bb8592683",
    "HTTPHeaders": {
      "transfer-encoding": "chunked",
      "date": "Wed, 23 May 2018 21:12:56 GMT",
      "connection": "close",
      "server": "AmazonEC2"
    }
  },
  "Error": {
    "Message": "resource sg-56532d2f has a dependent object",
    "Code": "DependencyViolation"
  }
}
```
