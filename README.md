# EmailAPI
## Setup
1. EmailAPI.py contains basic functions to send emails.
2. rest_apis.py contains the restapi for sending email.
3. Chalice is used to deploy on AWS.
4. test_emails.py contains the unittests.
5. create credentials.csv with below contents 
  
  Smtp Username,Smtp Password,SENDGRID_API_KEY,MAILGUN_API_KEY 
  AWSUSERNAME,AWSSES_PWD,SEND KEY,MAINGUN_APIKEY

## Libraries used.
1. Chalice for deploying on AWS.
2. sendgrid, smtplib,requests, etc.

## Commands
### Chalice commands
Chalice installs Python APP on AWS Lambda. 

1. pip install chalice -- to install chalice.
chalice new-project -- to create new chalice project.
chalice local -- to deploy services locally.
chalice deploy -- to deploy on AWS cloud using AWS Lambda.
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-west-2:928180933616:function:newProj-dev
  - Rest API URL: https://204q4esdki.execute-api.us-west-2.amazonaws.com/api/sendmail



## Deployments
### Local deployment
1. Run python rest_apis.py to get the local server IP. 
    Ex:  http://127.0.0.1:5000/
2. In new terminal run curl command to invoke rest commands.
Examples are in rest_commands.txt



**Description of parameters.**
1. "service_provider" -- can be "MAILGUN", "AWSSES", or "SENDGRID",
2. "sender" -- From email address.  
3. "recipient"  -- To email address. 
4. "subject": -- Subject of email.
5. "body":  -- Body in a HTML format.

