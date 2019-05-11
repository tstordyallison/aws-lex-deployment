# AWS Lex Deployment

## Description
Using the [AWS Boto Library](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html) deploy an AWS Lex Bot and Intents.

This code assumes there is one version of the code, $LATEST.  Versioning of bot and intents should be added.

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
This script takes two parameters:
1. The bot name
1. The directory location on where the intent config files are
```
AWS_DEFAULT_PROFILE=ffg-lex-bot AWS_DEFAULT_REGION=eu-west-1 python deployment_scripts/deploy.py MyBotName ./intents
```

### Delete
This script takes two parameters:
1. The bot name
1. The comma separated resources you want to delete, options are [bot, intent]
```
AWS_DEFAULT_PROFILE=ffg-lex-bot AWS_DEFAULT_REGION=eu-west-1 python deployment_scripts/delete.py MyBotName bot,intent
```

### Define intents
Under the intents directory:
* create a directory called the intent name
* create a file called config.json and create a JSON dict of the parameters for the [put_intent](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Client.put_intent) Boto function.
* TODO
