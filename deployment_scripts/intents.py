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
            config = json.load(cfg_file)

        response = client.put_intent(**config)

        print(response)
        print("Created/Updated intent %s" % config["name"])
        deployed_intent_names.append(config["name"])

    return deployed_intent_names


def delete(intent_names, _client=boto3.client):
    client = _client(CLIENT_NAME)

    for i in intent_names:
        client.delete_intent(name=i)
