# AWS Lex Deployment

## Description
Using the [AWS Boto Library](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html) deploy an AWS Lex Bot and Intents.

## Development
### Environment Setup
Install pip and virtualenv using the instructions at https://virtualenv.pypa.io/en/latest/installation/.
Run the following from your terminal:
```
#Create a virtual environment
virtualenv venv-lex-bot

#Activate the virtual environment
source ./venv-lex-bot/bin/activate

#Install project requirements
pip install -r requirements.txt
```

### Deploy
```
AWS_DEFAULT_PROFILE=ffg-lex-bot AWS_DEFAULT_REGION=eu-west-1 python deployment_scripts/deploy.py mybotname
```
