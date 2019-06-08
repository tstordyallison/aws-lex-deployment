import boto3
import json
import os

CLIENT_NAME="lex-models"


def deploy(intents_dir, _client=boto3.client):
    client = _client(CLIENT_NAME)
    intents = os.listdir(intents_dir)

    deployed_intent_names = []

    for i in intents:
        intent_config_path=os.path.join(intents_dir, i, "config.json")

        if not os.path.isfile(intent_config_path):
            raise Exception("Intent config file MISSING at path %s" % intent_config_path)

        with open(intent_config_path) as cfg_file:
            cfg_file_content = cfg_file.read()
            cfg_file_content = cfg_file_content.replace("{ReplaceWithAWSRegion}", os.environ["AWS_DEFAULT_REGION"])
            cfg_file_content = cfg_file_content.replace("{ReplaceWithAWSAccountId}", _client("sts").get_caller_identity()["Account"])
            print(cfg_file_content)
            config = json.loads(cfg_file_content)

        response = client.put_intent(**config)

        print(response)
        print("Created/Updated intent %s" % config["name"])
        deployed_intent_names.append(config["name"])

    return deployed_intent_names


def delete(intent_names, _client=boto3.client):
    client = _client(CLIENT_NAME)

    for i in intent_names:
        client.delete_intent(name=i)
