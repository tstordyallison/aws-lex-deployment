# AWS Lex Deployment

## Description

Using the [AWS Boto Library](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html) deploy an AWS Lex Bot and Intents.

This code assumes there is one version of the code, $LATEST.  Versioning of bot and intents should be added.

## Development

### Environment Setup

Install pipenv from [here](https://docs.pipenv.org/en/latest/). 

Run the following from your terminal:

```
pipenv install
```
 
This will pull your dependencies from pypi. 

If you want to activate the `virtualenv` for your shell:

```
pipenv shell
```

Note: The example commands below use `pipenv run` and don't require that you do this. 

### IAM User AWS Setup

You will need an IAM user that has permission deploy lambdas & lex. You can make this user with the provided Cloud Formation template.

In the AWS console:

1. Deploy the CloudFormation script `cloudformation/deployer_user.json` - this will create a new user.
1. Go into the IAM Service
1. Click on Users from the left hand side
1. Select the user created
1. Click on Security Credentials
1. Create and Download Access Key
1. Use this Access Key to create credentials on your laptop at `~/.aws/credentials` - as seen in the [AWS setup credentials guide](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).


### Deploy

Deploy the intents to a brand new bot in AWS from source. 

This script takes two parameters:

1. The bot name
1. The directory location on where the intent config files are.

```
AWS_DEFAULT_PROFILE=ffg-lex-bot AWS_DEFAULT_REGION=eu-west-1 pipenv run python -m aws_lex_deployment.deploy ./example-bots/MyBot --instance=MyName
```

### Delete

This script takes two parameters:

1. The bot name
1. The comma separated resources you want to delete, options are [bot, intent]

```
AWS_DEFAULT_PROFILE=ffg-lex-bot AWS_DEFAULT_REGION=eu-west-1 pipenv run python -m aws_lex_deployment.delete MyBotName bot,intent
```

### Define intents

Under the intents directory:

* create a directory called the intent name
* create a file called config.json and create a JSON dict of the parameters for the [put_intent](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lex-models.html#LexModelBuildingService.Client.put_intent) Boto function.
* TODO
