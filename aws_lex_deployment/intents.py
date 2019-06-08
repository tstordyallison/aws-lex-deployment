import boto3
import botocore
import json
import os

CLIENT_NAME="lex-models"


def deploy(intents_dir, instance=None):
    client = boto3.client(CLIENT_NAME)
    intents = os.listdir(intents_dir)

    deployed_intent_names = []

    for i in intents:
        intent_config_path=os.path.join(intents_dir, i, "config.json")

        if not os.path.isfile(intent_config_path):
            raise Exception("Intent config file MISSING at path %s" % intent_config_path)

        with open(intent_config_path) as cfg_file:
            config = json.load(cfg_file)

        intent_name = config["name"]

        if instance:
            # Let's prefix the intent name with the instance name, so we have different bots live side by side. 
            intent_name = instance + intent_name
            config["name"] = intent_name

        try:
            current_intent = client.get_intent(
                name=intent_name,
                version="$LATEST"
            )
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'NotFoundException':
                current_intent = None
            else:
                raise

        if os.path.isfile(os.path.join(intents_dir, i, "lambda.py")):
            aws_region = os.environ.get( "AWS_DEFAULT_REGION", 'eu-west-1' )
            aws_account = boto3.client("sts").get_caller_identity()["Account"]
            lambda_name = f"{intent_name}-Lambda"

            uri = f'arn:aws:lambda:{aws_region}:{aws_account}:function:{lambda_name}'
            config['fulfillmentActivity']['codeHook']['uri'] = uri

        # Just always update.
        if current_intent:
            config['checksum'] = current_intent['checksum']

        # Off to AWS!
        _response = client.put_intent(**config)

        print("Created/Updated intent %s" % intent_name)
        deployed_intent_names.append(intent_name)

    return deployed_intent_names


def delete(intent_name):
    client = boto3.client(CLIENT_NAME)
    client.delete_intent(name=intent_name)
